FROM python:3.7

RUN apt-get update && \
apt-get install -y --fix-missing python3-dev libjpeg-dev nginx supervisor pdftk && \
echo "daemon off;" >> /etc/nginx/nginx.conf && \
mkdir /var/log/api/ && \
rm -rf /var/lib/apt/lists/*

ENV DJANGO_SETTINGS_MODULE=api.settings.docker ENV=local DATABASE_URL="postgres://127.0.0.1:5432/sales-api"

WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install uvicorn gunicorn &&  pip install -r requirements.txt

COPY . /usr/src/app/

RUN bash -c "python manage.py check"

RUN bash -c "python manage.py collectstatic --noinput"

RUN bash -c "chmod +x ./docker/run.sh"

EXPOSE 8000 90

CMD ["./docker/run.sh"]
