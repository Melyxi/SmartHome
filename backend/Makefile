

run-dev-server: ## Run dev server 127.0.0.1:8000
	export DEBUG=True; uvicorn app:create_app --reload --host 0.0.0.0 --port 8000

run-prod-server: ## Run prod server 127.0.0.1:8000
	export DEBUG=False; uvicorn app:create_app --reload --host 0.0.0.0 --port 8000

alembic-upgrade-head: # Apply migrations for dev server
    export DEBUG=True; alembic upgrade head