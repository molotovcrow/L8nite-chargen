#!/bin/sh

python l8nite/manage.py makemigrations
python l8nite/manage.py migrate
python l8nite/manage.py runserver 0.0.0.0:${DJANGO_PORT}
