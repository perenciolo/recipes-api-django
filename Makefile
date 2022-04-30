.phony: create-app up test lint

create-app:
	UID=${UID} GID=${GID} docker-compose run app sh -c "django-admin startproject app ."

up:
	UID=${UID} GID=${GID} docker-compose up -d

test:
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "python manage.py test"

lint:
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "flake8"