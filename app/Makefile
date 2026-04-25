# Variables
COMPOSE_BASE = docker compose -f dockercompose.yml
COMPOSE_DEV = $(COMPOSE_BASE) -f dockercompose.dev.yml
COMPOSE_PROD = $(COMPOSE_BASE) -f dockercompose.prod.yml

SERVICE_API = api

# ----------------------
#  DEV
# ----------------------

up:
	$(COMPOSE_DEV) up --build

down:
	$(COMPOSE_DEV) down

restart:
	$(COMPOSE_DEV) down && $(COMPOSE_DEV) up --build

logs:
	$(COMPOSE_DEV) logs -f

ps:
	$(COMPOSE_DEV) ps

shell:
	$(COMPOSE_DEV) exec $(SERVICE_API) bash

env:
	$(COMPOSE_DEV) exec $(SERVICE_API) env | sort

# ----------------------
#  CLEAN
# ----------------------

clean:
	$(COMPOSE_DEV) down -v --remove-orphans

prune:
	docker system prune -f

# ----------------------
# 🐘 DB
# ----------------------

db:
	$(COMPOSE_DEV) exec db psql -U postgres -d examdb

# ----------------------
# 🚀 PROD (sin override)
# ----------------------

prod-up:
	$(COMPOSE_PROD) up -d --build

prod-down:
	$(COMPOSE_PROD) down

prod-logs:
	$(COMPOSE_PROD) logs -f