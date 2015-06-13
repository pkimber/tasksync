from setuptools import setup

setup(
    name='tasksync',
    version='0.1',
    py_modules=['tasksync'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tasksync=tasksync:cli
    ''',
)
