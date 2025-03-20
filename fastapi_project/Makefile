build:
	docker compose build
	
start: build
	docker compose up -d --force-recreate

down:
	docker compose down --volumes

test: build
	docker compose run --rm --entrypoint="" api poetry run pytest -vvv

logs:
	docker compose logs -f

api-logs:
	docker compose logs -f api