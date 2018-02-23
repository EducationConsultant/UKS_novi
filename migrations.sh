#!/bin/sh
sleep 15 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8027
exec "$@"
