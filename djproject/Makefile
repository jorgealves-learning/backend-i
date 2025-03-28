# MAC and WINDOWS Users USE DEV CONTAINER

# LINUX Users DO NOT USE DEV CONTAINER
#             ------------------------

migrations:
	poetry run python manage.py makemigrations

create-superuser:
	poetry run python manage.py createsuperuser

compose.start:
	docker compose up --build --force-recreate

compose.migrate:
	docker compose run --rm web poetry run python manage.py migrate

compose.collectstatic:
	docker compose exec web poetry run python manage.py collectstatic --noinput