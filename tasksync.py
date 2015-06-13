# -*- encoding: utf-8 -*-
import click
import yaml

from tasklib.task import (
    Task,
    TaskWarrior,
)

CYAN = 'cyan'
YELLOW = 'yellow'
WHITE = 'white'

SETTINGS_FILE = '.private.yaml'

#        data_location = settings.TASKWARRIOR
#        print(settings.TASKWARRIOR)
#        tw = TaskWarrior(data_location)
#
#        tw.config.update({'uda.ticket.type': 'numeric'})
#        tw.config.update({'uda.site.type': 'string'})
#
#        items = tw.tasks.pending().filter(ticket=99, project='pkimber_net')
#        for item in items:
#            print(item['description'], item['project'], item['ticket'], item['uuid'])
#        #Task(
#        #    tw,
#        #    description="Testing task",
#        #    site='pkimber_net',
#        #    ticket=99,
#        #    project='pkimber_net',
#        #).save()
#
#
#        #tasks = tw.tasks.pending()
#        #for task in tasks:
#        #    print(task['uuid'])
#        #    print(task)
#        #uuid = '5de8e3bf-c2af-4455-a0b4-d61effeba82d'
#        #task = tw.tasks.get(uuid=uuid)
#        #print()
#        #print('task: {}'.format(task))
#        #ticket = Ticket.objects.get(pk=38)
#        #print('ticket: {}'.format(ticket))
#        #try:
#        #    ticket_task = TicketTaskWarrior.objects.get(uuid=uuid)
#        #    print('found: {}'.format(ticket_task))
#        #    print('     : {}'.format(ticket_task.uuid))
#        #except TicketTaskWarrior.DoesNotExist:
#        #    ticket_task = TicketTaskWarrior.objects.create_taskwarrior(
#        #        uuid=task['uuid'],
#        #        ticket=ticket,
#        #    )
#        #    print('create: {}'.format(ticket_task))
#        #ticket = Ticket.objects.get(pk=764)
#        #print()
#        #print(ticket.title)
#        print("TaskWarrior complete...")

def temp_yaml_write():
    """Check YAML format."""
    data = {
        'kb': {
            'project': 'kb',
            'username': 'patrick',
            'password': 'xyz',
            'url': 'http://localhost:8000',
        },
    }
    with open(SETTINGS_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def settings():
    data = yaml.load(open(SETTINGS_FILE, "r"))
    return data


@click.command()
def cli():
    click.clear()
    click.secho('Sync TaskWarrior with CRM', fg=WHITE, bold=True)
    temp_yaml_write()
    data = settings()
    for site, setting in data.items():
        click.secho('{}'.format(site), fg=CYAN)


if __name__ == '__main__':
    cli()
