dev:
	uv run python3 manage.py runserver

translate:
	uv run django-admin makemessages --locale ru
	uv run python manage.py compilemessages

migrate:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

tests:
	uv run python3 manage.py test

install:
	uv sync

lint:
	uv run flake8 task_manager

build:
	./build.sh

render-start:
	.venv/bin/gunicorn --bind 0.0.0.0:$$PORT task_manager.wsgi

collectstatic:
	uv run python manage.py collectstatic --noinput