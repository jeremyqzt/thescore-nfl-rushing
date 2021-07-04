#!/bin/sh

until cd /app/nflrushing
do
    echo "Waiting for server volume..."
done

until python ./manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python ./manage.py loaddata --file ./api/management/files/rushing.json
python ./manage.py collectstatic --noinput

gunicorn nflrushing.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4