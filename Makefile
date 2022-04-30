.phony: create-app up test lint build

create-app:
	UID=${UID} GID=${GID} docker-compose run app sh -c "django-admin startproject app ."

build:
	UID=${UID} GID=${GID} docker-compose up --build --force-recreate -d

up:
	UID=${UID} GID=${GID} docker-compose up -d

test:
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "python manage.py test"

lint:
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "autopep8 --in-place --aggressive --aggressive /app/**/*.py"
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "flake8"