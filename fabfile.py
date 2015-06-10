import os

from fabric.api import run, env, cd, abort, sudo
from fabric.contrib.console import confirm


def dev():
    env.hosts = ['7webpages@7webpages.com']
    env.directory = '/home/7webpages/ironcoderprojects/infinity/'
    env.activate = 'source ' + os.path.join(env.directory, '.env/bin/activate')
    env.branch = 'master'
    env.supervisor_app_name = 'infinity'
    env.requirements = 'requirements.txt'


def virtualenv(command):
    with cd(env.directory):
        run(env.activate + '&&' + command)


def deploy():
    virtualenv('git checkout %s' % env.branch)
    virtualenv('git pull origin %s' % env.branch)
    virtualenv('pip install -r %s%s' % (
        env.directory, env.requirements))
    virtualenv('python xybid/manage.py syncdb')
    virtualenv('python xybid/manage.py migrate')
    virtualenv('python xybid/manage.py collectstatic')
    run('sudo /usr/bin/supervisorctl restart %s' % env.supervisor_app_name)
