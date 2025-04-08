dev_run:
	@python ./ai_chat_api/app.py

dev_run_worker:
	@celery -A ai_chat_api.celery_app worker --loglevel=info

dev_install:
	@pip install -e .

check_code:
	@flake8 .

test:
	make init_db
	pytest tests --cov-report=xml:./reports/tests_coverage.xml --cov-report term

test_integration:
	make init_db
	pytest tests_integration --cov-report=xml:./reports/api_coverage.xml --cov-report term

init_db:
	@ai_chat_api_cli init-db
