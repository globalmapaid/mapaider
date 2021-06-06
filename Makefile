ifneq (,$(wildcard ./.env))
   include .env
   export
   ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up --build --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

migrate:
	docker-compose exec wemod-api python3 manage.py migrate --noinput

makemigrations:
	docker-compose exec wemod-api python3 manage.py makemigrations

showmigrations:
	docker-compose exec wemod-api python3 manage.py showmigrations

superuser:
	docker-compose exec wemod-api python3 manage.py createsuperuser

down-v:
	docker-compose down -v

volume:
	docker volume inspect wemod-project_postgres_data

