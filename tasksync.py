# -*- encoding: utf-8 -*-
import click
import logging
import requests
import yaml

from datetime import datetime

from tasklib.task import (
    Task,
    TaskWarrior,
)


logger = logging.getLogger(__name__)

CYAN = 'cyan'
GREEN = 'green'
YELLOW = 'yellow'
RED = 'red'
WHITE = 'white'

CRM_API_VERSION = '0.1'
CONFIG_FILE = '.private.yaml'

PRIORITY = {
    'High': 'H',
    'Medium': 'M',
}


class SyncError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('{}, {}'.format(self.__class__.__name__, self.value))


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

def json_headers(token):
    return {
        'Content-type': 'application/json',
        'Authorization': 'Token {}'.format(token),
    }


def get_json(url, token):
    response = requests.get(url, headers=json_headers(token))
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise ServiceUnauthorized(response.status_code)
    elif response.status_code == 404:
        raise DoesNotExistError('{}: {}'.format(response.reason, url))
    else:
        log_error('get_json', 'GET', url, response)


def load_config():
    data = yaml.load(open(CONFIG_FILE, "r"))
    return data


def log_error(name, verb, url, response):
    message = "'{}' {} [data: '{}...']".format(
        url, response.status_code, response.text[:1000]
    )
    logger.error('{}: {}'.format(name, message))
    logger.error(message)
    raise SyncError(
        "Cannot {} json data: {}".format(verb, message)
    )


def login(url, user_name, password):
    """login using a form post."""
    token = None
    data = {'username': user_name, 'password': password}
    try:
        response = requests.post(url_login(url), data=data)
    except requests.ConnectionError as e:
        raise SyncError('Cannot connect to {}'.format(api_url)) from e
    if response.status_code == 200:
        token = response.json().get('token')
    else:
        raise SyncError('Invalid Login ({}: {}) {}'.format(
            response.status_code,
            response.reason,
            response.text[:100]
        ))
    return token


def temp_yaml_write():
    """Check YAML format."""
    data = {
        'data_location': '/home/patrick/task',
        'sites': {
            'kb': {
                'project': 'kb',
                'username': 'patrick',
                'password': 'xyz',
                'url': 'http://localhost:8000',
            },
        },
    }
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def tickets(url, token, tw, project):
    url = '{}ticket'.format(url_api(url))
    data = get_json(url, token)
    for item in data:
        description = '{} {}'.format(item['contact'].upper(), item['title'])
        due = datetime.strptime(item['due'], '%Y-%m-%d')
        priority = PRIORITY[item['priority']]
        ticket = int(item['id'])
        username = item['username']

        update = False
        alert = ''
        message = ''
        click.secho('  {:06d}'.format(ticket), fg=YELLOW, bold=True, nl=False)
        task = tw.tasks.get(project=project, ticket=ticket)
        if task['due'].date() != due.date():
            task['due'] = due.date()
            update = True
        if task['priority'] != priority:
            task['priority'] = priority
            update = True
        if task['description'] != description:
            task['description'] = description
            update = True
        if task[''] != username:
            task['username'] = username
            update = True
        #task = tw.tasks.get(project=project, ticket=ticket)
        if task.completed or task.deleted:
            task['status'] = 'pending'
            alert = 'was completed (or deleted) - now pending'
            update = True
            #click.secho('was completed or deleted - now pending', fg=YELLOW, bold=True)
        if update:
            message = 'update'
            task.save()
        click.secho('  ', nl=False)
        click.secho(u'\u2713'.format(ticket), fg=GREEN, bold=True, nl=False)
        click.secho('  ', nl=False)
        click.secho('{:20s}'.format(message), nl=False)
        click.secho('{:20s}'.format(alert), fg=RED, bold=True, nl=False)
        click.secho('')

        #Task(
        #    tw,
        #    description=item['title'],
        #    project=project,
        #    ticket=item['id'],
        #    username=item['username'],
        #).save()
        #tasks = tw.tasks.filter(project=project)

        #try:
        #    task = tw.tasks.get(status='pending', project=project, ticket=ticket)
        #except Task.DoesNotExist:
        #    click.secho('Task DoesNotExist', fg=RED, bold=True)

        click.secho('  {}'.format(item))
        #for task in tasks:
        click.secho('    {}'.format(task['uuid']))
        click.secho('      {}'.format(task['description']))
        click.secho('      {}'.format(task['project']))
        click.secho('      {}'.format(task['ticket']))
        click.secho('      {}'.format(task['username']))
        click.secho('      {}'.format(task['due']))
        break


def url_api(url):
    """Return the API URL.

    e.g. https://www.hatherleigh.info/api/0.1/

    """
    if not url.endswith('/'):
        url = url + '/'
    return '{}api/{}/'.format(url, CRM_API_VERSION)


def url_login(url):
    """Return the login URL."""
    if not url.endswith('/'):
        url = url + '/'
    return '{}token/'.format(url)


@click.command()
def cli():
    click.clear()
    click.secho('Sync TaskWarrior with CRM', fg=WHITE, bold=True)
    #temp_yaml_write()
    config = load_config()
    # TaskWarrior
    data_location = config['data_location']
    tw = TaskWarrior(data_location)
    tw.config.update({'uda.ticket.type': 'numeric'})
    tw.config.update({'uda.site.type': 'string'})
    tw.config.update({'uda.username.type': 'string'})
    # Sites
    sites = config['sites']
    for project, data in sites.items():
        click.secho('{}'.format(project), fg=CYAN, bold=True)
        # login
        url = data['url']
        token = login(url, data['username'], data['password'])
        click.secho('  login')
        # tickets
        tickets(url, token, tw, project)


if __name__ == '__main__':
    cli()
