#!/bin/sh
sleep 15 
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py runserver 0.0.0.0:8027
exec "$@"
