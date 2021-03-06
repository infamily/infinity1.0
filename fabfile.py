import os

from fabric.api import run, env, cd, abort, sudo
from fabric.contrib.console import confirm


def dev():
    env.hosts = ['infty@api.infty.xyz']
    env.directory = '/home/infty/infinity/'
    env.activate = 'source ' + os.path.join(env.directory, '.env/bin/activate')
    env.branch = 'dev'
    env.supervisor_app_name = 'infty'
    env.requirements = 'requirements.txt'


def prod():
    env.hosts = ['infty@infty.xyz']
    env.directory = '/home/infty/infinity/'
    env.activate = 'source ' + os.path.join(env.directory, '.env/bin/activate')
    env.branch = 'master'
    env.supervisor_app_name = 'infty'
    env.requirements = 'requirements.txt'


def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)


def deploy():
    virtualenv('git checkout %s' % env.branch)
    virtualenv('git pull origin %s' % env.branch)
    virtualenv('pip install -r %s%s' % (
        env.directory, env.requirements))
    virtualenv('python src/manage.py migrate --noinput')
    virtualenv('python src/manage.py collectstatic --noinput')
    # uncomment it when deploy project first time
    # loading fixtures takes additional time, will be really long
    # virtualenv('python infinity/manage.py loaddata fixtures/languages.json')
    # virtualenv('python infinity/manage.py loaddata fixtures/needs.json.gz')
    run('sudo /usr/bin/supervisorctl restart %s' % env.supervisor_app_name)
