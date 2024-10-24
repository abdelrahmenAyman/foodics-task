# Variables
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_FILE := docker-compose.yml
DOCKER_COMPOSE_TEST_FILE := docker-compose.test.yml

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: run
run: ## Start the server
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up

.PHONY: run-detached
run-detached:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: test
test: ## Run tests
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_TEST_FILE) up --abort-on-container-exit

.PHONY: build
build: ## Build the Docker image
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

.PHONY: build-test
build-test: ## Build the test Docker image
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_TEST_FILE) build

.PHONY: stop
stop: ## Stop all running containers
	$(DOCKER_COMPOSE) down

.PHONY: down
down: stop ## Remove all containers, networks, and volumes
	$(DOCKER_COMPOSE) down -v

.PHONY: seed-db
seed-db:
	docker compose exec web python app/scripts/seed_db.py

.PHONY: drop-db
drop-db:
	docker-compose down
	docker volume rm foodics_task_postgres_data

.PHONY: clean
clean: ## Clean up cache and compiled files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
