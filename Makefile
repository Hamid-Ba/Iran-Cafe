build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

stop:
	docker compose -f local.yml stop

restart:
	docker compose -f local.yml restart

show_logs:
	docker compose -f local.yml logs

migrate:
	docker compose -f local.yml run --rm cafeiran_api python manage.py migrate

makemigrations:
	docker compose -f local.yml run --rm cafeiran_api python manage.py makemigrations

collectstatic:
	docker compose -f local.yml run --rm cafeiran_api python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm cafeiran_api python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

flake8:
	docker compose -f local.yml exec cafeiran_api flake8 .

black-check:
	docker compose -f local.yml exec cafeiran_api black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec cafeiran_api black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec cafeiran_api black --exclude=venv .

test:
	docker compose -f local.yml run --rm cafeiran_api python manage.py test

build_p:
	docker compose -f production.yml up --build -d --remove-orphans

up_p:
	docker compose -f production.yml up -d

down_p:
	docker compose -f production.yml down

stop_p:
	docker compose -f production.yml stop

restart_p:
	docker compose -f production.yml restart

show_logs_p:
	docker compose -f production.yml logs

migrate_p:
	docker compose -f production.yml run --rm cafeiran_api python manage.py migrate

makemigrations_p:
	docker compose -f production.yml run --rm cafeiran_api python manage.py makemigrations

collectstatic_p:
	docker compose -f production.yml run --rm cafeiran_api python manage.py collectstatic --no-input --clear

superuser_p:
	docker compose -f production.yml run --rm cafeiran_api python manage.py createsuperuser

down-v_p:
	docker compose -f production.yml down -v