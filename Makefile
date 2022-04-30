.phony: create-app

create-app:
	docker-compose run app sh -c "django-admin startproject app ."