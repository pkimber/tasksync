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
