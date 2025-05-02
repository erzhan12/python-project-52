#!/usr/bin/env bash
set -e

echo "Скачиваем uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.local/bin/env

echo "Устанавливаем gunicorn..."
pip3 install gunicorn

echo "Синхронизируем зависимости..."
make install

echo "Компилируем переводы..."
uv run python manage.py compilemessages
make translate
echo "Собираем статику..."
make collectstatic

echo "Применяем миграции..."
make migrate

echo "Build script выполнен успешно."