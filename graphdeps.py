#!/usr/bin/env python
'graph dependencies in projects'
import json
from subprocess import Popen, PIPE
import sys
import textwrap



# Typical command line usage:
#
# python graphdeps.py TASKFILTER
#
# TASKFILTER is a taskwarrior filter, documentation can be found here: http://taskwarrior.org/projects/taskwarrior/wiki/Feature_filters
#
# Probably the most helpful commands are:
#
# python graphdeps.py project:fooproject status:pending   
#  --> graph pending tasks in project 'fooproject'
#
# python graphdeps.py project:fooproject
#  --> graphs all tasks in 'fooproject', pending, completed, deleted
# 
# python graphdeps.py status:pending
#  --> graphs all pending tasks in all projects
#
# python graphdeps.py
#  --> graphs everything - could be massive
#


#Wrap label text at this number of characters
charsPerLine = 20;


#full list of colors here: http://www.graphviz.org/doc/info/colors.html
blockedColor = 'gold4'
maxUrgencyColor = 'red2' #color of the tasks that have absolutely the highest urgency
unblockedColor = 'green'
doneColor = 'grey'
waitColor = 'white'
deletedColor = 'pink';

#The width of the border around the tasks:
penWidth = 1



#Have one HEADER (and only one) uncommented at a time, or the last uncommented value will be the only one considered

#Left to right layout, my favorite, ganntt-ish
HEADER = "digraph  dependencies { splines=true; overlap=ortho; rankdir=LR; weight=2;"

#Spread tasks on page
#HEADER = "digraph  dependencies { layout=neato;   splines=true; overlap=scalexy;  rankdir=LR; weight=2;"

#More information on setting up graphviz: http://www.graphviz.org/doc/info/attrs.html


#-----------------------------------------#
#  Editing under this might break things  #
#-----------------------------------------#

FOOTER = "}"

JSON_START = '['
JSON_END = ']'

validUuids = list()



def call_taskwarrior(cmd):
    'call taskwarrior, returning output and error'
    tw = Popen(['task'] + cmd.split(), stdout=PIPE, stderr=PIPE)
    return tw.communicate()

def get_json(query):
    'call taskwarrior, returning objects from json'
    result, err = call_taskwarrior('export %s' % query)
    return json.loads(JSON_START + result + JSON_END)

def call_dot(instr):
    'call dot, returning stdout and stdout'
    dot = Popen('dot -T png'.split(), stdout=PIPE, stderr=PIPE, stdin=PIPE)
    return dot.communicate(instr)

if __name__ == '__main__':
    query = sys.argv[1:]
    print ('Calling TaskWarrior')
    data = get_json(' '.join(query))
    #print data
    
    maxUrgency = -9999;
    for datum in data:
        if float(datum['urgency']) > maxUrgency:
            maxUrgency = float(datum['urgency'])


    # first pass: labels
    lines = [HEADER]
    print ('Printing Labels')
    for datum in data:
        validUuids.append(datum['uuid'])
        if datum['description']:

            style = ''
            color = ''
            style = 'filled'

            if datum['status']=='pending':
                prefix = datum['id']
                if not datum.get('depends','') : color = unblockedColor
                else :
                    hasPendingDeps = 0
                    for depend in datum['depends'].split(','):
                        for datum2 in data:
                            if datum2['uuid'] == depend and datum2['status'] == 'pending':
                               hasPendingDeps = 1
                    if hasPendingDeps == 1 : color = blockedColor
                    else : color = unblockedColor

            elif datum['status'] == 'waiting':
                prefix = 'WAIT'
                color = waitColor
            elif datum['status'] == 'completed':
                prefix = 'DONE'
                color = doneColor
            elif datum['status'] == 'deleted':
                prefix = 'DELETED'
                color = deletedColor
            else:
                prefix = ''
                color = 'white'


            if float(datum['urgency']) == maxUrgency:
                color = maxUrgencyColor

            label = '';
            descriptionLines = textwrap.wrap(datum['description'].replace('"', "'"),charsPerLine);
            for descLine in descriptionLines:
                label += descLine+"\\n";
    
            lines.append('"%s"[shape=box][penwidth=%d][label="%s\:%s"][fillcolor=%s][style=%s]' % (datum['uuid'], penWidth, prefix, label, color, style))
            #documentation http://www.graphviz.org/doc/info/attrs.html



    # second pass: dependencies
    print ('Resolving Dependencies')
    for datum in data:
        if datum['description']:
            for dep in datum.get('depends', '').split(','):
                #print ("\naaa %s" %dep)
                if dep!='' and dep in validUuids:
                    lines.append('"%s" -> "%s";' % (dep, datum['uuid']))
                    continue

    lines.append(FOOTER)

    #with open('temp.out', 'w') as f:
    #    for item in lines:
    #        f.write(item)
    #        f.write('\n')

    print ('Calling dot')
    png, err = call_dot('\n'.join(lines))
    if err != '':
        print ('Error calling dot:')
        print (err.strip())

    print ('Writing to deps.png')
    with open('deps.png', 'w') as f:
        f.write(png)
