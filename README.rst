TaskSync
********

Synchronise our CRM system to a TaskWarrior database.

Install
=======

Virtual Environment
-------------------

::

  pyvenv-3.4 --without-pip venv-tasksync
  source venv-tasksync/bin/activate
  wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
  python get-pip.py

  pip install -r requirements.txt

Configuration
=============

Create a ``.private.yaml`` file in the root of this project and configure:

.. code-block:: yaml

  data_location: /home/patrick/task
  sites:
    hatherleigh:
      password: your-password
      url: https://www.hatherleigh.info
      username: patrick

- ``data_location`` is the folder containing your TaskWarrior data.
- ``sites`` is a list of web sites which have the API enabled for our CRM.
  For more information, see https://www.pkimber.net/open/app-crm.html
- replace ``hatherleigh`` with the name you want TaskWarrior to use for your
  project.
- ``username`` and ``password`` are your login details for the web site.
- ``url`` is the URL of your web site.

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  tasksync

To create a diagram::

  python2 graphdeps.py project:hatherleigh status:pending

Or... using https://github.com/vsbabu/pinboard::

  git clone git@github.com:vsbabu/pinboard.git
  cd pinboard

  # js board
  python2 utils/export-yaml-pinboard.py kb > board.js.yml
  # edit 'board.js.yml' to remove square brackets (open and close)
  firefox index.html

  # or... html
  python2 utils/export-html-pinboard.py kb biz personal > out.html
  firefox out.html
