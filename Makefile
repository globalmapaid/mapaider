ifneq (,$(wildcard ./.env))
   include .env
   export
   ENV_FILE_PARAM = --env-file .env
endif

build:
	docker compose up -d --build --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

migrate:
	docker compose exec mapaider-api python3 manage.py migrate --noinput

makemigrations:
	docker compose exec mapaider-api python3 manage.py makemigrations

showmigrations:
	docker compose exec mapaider-api python3 manage.py showmigrations

superuser:
	docker compose exec mapaider-api python3 manage.py createsuperuser

down-v:
	docker compose down -v

volume:
	docker volume inspect wemod-project_postgres_data

test:
	docker compose exec mapaider-api pytest

test-file:
	docker compose exec mapaider-api pytest $(FILE)

test-k:
	docker compose exec mapaider-api pytest -k "$(K)"

test-node:
	docker compose exec mapaider-api pytest $(NODE)

TEST_MAP_SLUG ?= river-of-flowers

test-e2e:
	cd e2e && TEST_MAP_SLUG=$(TEST_MAP_SLUG) npx playwright test

test-e2e-headed:
	cd e2e && TEST_MAP_SLUG=$(TEST_MAP_SLUG) npx playwright test --headed

playwright-install:
	cd e2e && npm install && npx playwright install chromium

