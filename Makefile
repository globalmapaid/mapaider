ifneq (,$(wildcard ./.env))
   include .env
   export
   ENV_FILE_PARAM = --env-file .env
endif

build:
	docker-compose up -d --build --remove-orphans

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

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

