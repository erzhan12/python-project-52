install:
	uv sync

lint:
	uv run flake8 .

build:
	./build.sh