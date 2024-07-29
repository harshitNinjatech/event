# Makefile

# Define Python interpreter
PYTHON = pipenv run python

# Define Django project name (replace 'event' with your actual Django project name)
DJANGO_PROJECT = event
APP_NAME = main

# Install dependencies from Pipfile
install:
	pipenv install

# Apply database migrations
migrate:
	$(PYTHON) manage.py migrate

# Run Django development server
run:
	$(PYTHON) manage.py runserver

# Fetch and save events using Django management command
fetch_events:
	$(PYTHON) manage.py fetch_save_event"

# Start Celery worker
celery_worker:
	pipenv run celery -A $(DJANGO_PROJECT) worker --loglevel=info

# Start Celery beat scheduler
celery_beat:
	pipenv run celery -A $(DJANGO_PROJECT) beat --loglevel=info

# Install pre-commit hooks
setup_precommit:
	pipenv run pre-commit install

# Run pre-commit checks
pre_commit:
	pipenv run pre-commit run --all-files
