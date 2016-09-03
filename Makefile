export PYTHONWARNINGS=ignore
export DJANGO_SETTINGS_MODULE=conf.local

env:
	virtualenv .env
	pip install -r requirements.txt
	npm install -g bower

prepare:
	.env/bin/python src/manage.py bower install
	.env/bin/python src/manage.py collectstatic

shell:
	.env/bin/python src/manage.py shell

runserver:
	.env/bin/python src/manage.py runserver

test:
	.env/bin/python src/manage.py test --settings=conf.test

coverage:
	coverage run src/manage.py test --settings=conf.test

coverage-report:
	coverage html

wsgi:
	uwsgi\
		--http 127.0.0.1:8000\
		--need-app\
		--disable-logging\
		--wsgi-file src/wsgi.py\
		--processes 1\
		--threads 5\
		--py-autoreload 1\
		--home .env

clean:
	@echo "--> Cleaning pyc files"
		find . -name "*.pyc" -delete
