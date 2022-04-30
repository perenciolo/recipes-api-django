.phony: create-app up test lint build sh logs

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
	UID=${UID} GID=${GID} docker-compose run --rm app sh -c "flake8 --ignore=E501"

sh:
	UID=${UID} GID=${GID} docker-compose exec app sh -c "$(ARGS)"

logs:
	UID=${UID} GID=${GID} docker-compose logs app