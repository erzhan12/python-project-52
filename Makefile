dev:
	uv run python manage.py runserver

translate:
	uv run django-admin makemessages --locale ru
	uv run python manage.py compilemessages

migrate:
	uv run python manage.py makemigrations
	uv run python manage.py migrate

tests:
	uv run python manage.py test

install:
	uv sync

build:
	./build.sh

render-start:
	.venv/bin/gunicorn --bind 0.0.0.0:$$PORT task_manager.wsgi

collectstatic:
	uv run python manage.py collectstatic --noinput