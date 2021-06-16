#!/usr/bin/env bash
echo "~***** Working with migrations *****~"
pipenv run python src/manage.py migrate
echo "~***** Loading fixtures *****~"
pipenv run python src/manage.py loaddata groups.json
echo "~***** Start server *****~"
pipenv run python src/manage.py runserver 0.0.0.0:8000