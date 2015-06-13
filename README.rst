TaskSync
********

Synchronise our CRM systems to a TaskWarrior database.

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

Testing
=======

::

  find . -name '*.pyc' -delete
  py.test -x

Usage
=====

::

  tasksync
