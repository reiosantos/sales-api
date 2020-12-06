#!/bin/bash

if [[ $ENV == 'local' ]]; then
	echo "ENV LOCAL -------------------"
	python manage.py makemigrations
	python manage.py migrate --noinput
	python manage.py loaddata api/fixtures/*.json
	python manage.py collectstatic --noinput
	uvicorn api.asgi:application --reload --use-colors --host 0.0.0.0 --port 8000
else
	cp /usr/src/app/nginx.conf /etc/nginx/conf.d/default.conf
	cp /usr/src/app/supervisor.conf /etc/supervisor/conf.d/
	supervisord -n
fi
