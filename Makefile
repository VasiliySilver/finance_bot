.PHONY: run db

run:
	poetry run python main.py

db:
	docker compose -f docker/docker-compose.yml up -d