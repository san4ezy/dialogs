build:
	docker-compose build

up:
	docker-compose up -d

up_prod:
	docker-compose up -f docker-compose.prod.yml --build -d

down:
	docker-compose down

rebuild: down up

deep_rebuild:
	docker-compose down && docker-compose build --no-cache && docker-compose up -d

stop:
	docker-compose stop

start:
	docker-compose start

restart: stop start

ps:
	docker-compose ps

logs:
	docker-compose logs -f --tail 100 app

all_logs:
	docker-compose logs -f --tail 100

migrations:
	docker-compose exec app python manage.py makemigrations

migrate:
	docker-compose exec app python manage.py migrate

shell:
	docker-compose exec app python manage.py shell

bash:
	docker-compose exec app bash

populate:
	docker-compose exec app python manage.py populate

startapp:
	echo $(name)
