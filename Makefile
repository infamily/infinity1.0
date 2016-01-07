run-wsgi:
	uwsgi --http 127.0.0.1:8000 --need-app --disable-logging --wsgi-file src/wsgi.py --processes 1 --threads 5 --home .env
