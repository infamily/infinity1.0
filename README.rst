infinity
====================================

Installation instructions

System packages

sudo apt-get update && sudo apt-get dist-upgrade

sudo apt-get install gcc-snapshot build-essential

apt-get install postgresql postgresql-server-dev-9.3 nginx supervisor git-core libffi-dev

easy_install pip
pip install uwsgi virtualenv

Create infty user

> sudo su
> sudo useradd infty -m -s /bin/bash
> su infty
> ssh-keygen

Allow to run sudo supervisorctl command without password for xybid user

echo "infty ALL=(ALL) NOPASSWD: /usr/bin/supervisorctl" >> /etc/sudoers

Create postgresql User and database

> sudo su
> su postgres
> psql

postgres=# CREATE DATABASE infty;
CREATE DATABASE
postgres=# CREATE USER infty WITH PASSWORD 'infty';
CREATE ROLE
postgres=# GRANT ALL privileges ON DATABASE infty TO infty;
GRANT
postgres=# \q

Project setup

su infty

git clone git@bitbucket.org:7webpages/xybid.git

Set up virtualenv

cd ~/infty/infinity/
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt

Set up nginx configuration

sudo su

ln -s /home/infty/infinity/conf/prod/nginx.conf /etc/nginx/sites-enabled/infty.conf

Set up supervisor configuration

ln -s /home/infty/infinity/conf/prod/supervisor.conf /etc/supervisor/conf.d/infty.conf

Reload supervisor

supervisorctl reload

Make fab dev deploy from your local repository
