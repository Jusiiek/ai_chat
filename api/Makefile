dev_run:
	@python ./ai_chat_api/app.py

dev_install:
	@pip install -e .

check_code:
	@flake8 .

test_unit:
	make init_db
	pytest tests_unit --cov-report=xml:./reports/unit_coverage.xml --cov-report term

test_integration:
	make init_db
	pytest tests_integration --cov-report=xml:./reports/integration_coverage.xml --cov-report term

init_db:
	@ai_chat_api_cli init-db
