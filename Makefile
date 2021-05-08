DATABASE_URL?=postgresql://username:password@127.0.0.1/desafio

TAG?=latest

IMAGE_NAME:=desafio

################################# DOCKER #################################

docker-compose-rebuild: clean
	docker-compose down && docker-compose up -d --build

docker-build: clean
	docker build -t $(IMAGE_NAME):$(TAG) .

################################# LINT #################################

lint:
	mypy ./
	black ./
	flake8

################################# TESTS #################################

test: clean
	pytest -vv

################################# DATABASE MIGRATION #################################

db-revision:
	PYTHONPATH=. alembic revision -m $(m) --autogenerate

db-upgrade:
	PYTHONPATH=. alembic upgrade head

################################# CI #################################

dependencies:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python
	/opt/poetry/bin/poetry config virtualenvs.create false
	/opt/poetry/bin/poetry install --no-root

################################# CLEANER #################################

.clean-python: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.py.bak' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-lib: ## remove lib artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/
	rm -fr .mypy_cache/

clean: .clean-python .clean-lib

all: clean lint test
