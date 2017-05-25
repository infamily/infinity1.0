# Local development
```
git clone git@github.com:wefindx/infinity.git
cp src/conf/local.example.py src/conf/local.py
```

## pip deps
```
virtualenv -ppython2 .env
. .env/bin/activate
pip install -r requirements.txt
```

## postgresql

```
create database, e.g., infty
psql infty < infty.sql (if have dump, or migrate: python src/manage.py migrate)
# edit src/conf/local.py to set the existing database name / user in DATABASES
```

## front-end

```
npm i
sudo npm install -g bower
# whereis bower, and set its location to src/conf/local.py ( BOWER_PATH )
python src/manage.py bower_install
```

## run local server
```
python src/manage.py runserver
```

## add site, if needed
```
>>> from django.contrib.sites.models import Site
>>> Site.objects.create(name='localhost', domain='localhost')
```
