install:
	uv sync

lint:
	uv run flake8 hexlet_code task_manager

build:
	./build.sh

collectstatic:
	python manage.py collectstatic --no-input

migrate:
	python manage.py migrate

render-start:
	gunicorn hexlet_code.wsgi