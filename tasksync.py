# -*- encoding: utf-8 -*-
import click
import requests
import yaml

from tasklib.task import (
    Task,
    TaskWarrior,
)

CYAN = 'cyan'
YELLOW = 'yellow'
WHITE = 'white'

CRM_API_VERSION = '0.1'
CONFIG_FILE = '.private.yaml'


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


def load_config():
    data = yaml.load(open(CONFIG_FILE, "r"))
    return data


def login(api_url, user_name, password):
    """login using a form post."""
    token = None
    data = {'username': user_name, 'password': password}
    try:
        response = requests.post(url_login(api_url), data=data)
    except requests.ConnectionError as e:
        raise SyncError('Cannot connect to {}'.format(api_url)) from e
    if response.status_code == 200:
        token = response.json().get('token')
    else:
        raise SyncError('Invalid Login')
    return token


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
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def url_api(url):
    """Return the API URL.

    e.g. https://www.hatherleigh.info/api/0.1/

    """
    if not url.endswith('/'):
        url = url + '/'
    return '{}api/{}/'.format(url, CRM_API_VERSION)


def url_login(api_url):
    """Return the login URL."""
    return '{}token/'.format(url_api(api_url))


@click.command()
def cli():
    click.clear()
    click.secho('Sync TaskWarrior with CRM', fg=WHITE, bold=True)
    temp_yaml_write()
    config = load_config()
    for site, data in config.items():
        click.secho('{}'.format(site), fg=CYAN)
        url = url_api(data['url'])
        token = login(url, data['username'], data['password'])


if __name__ == '__main__':
    cli()
