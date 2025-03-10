#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
#pip install -r requirements.txt
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
make install
# Convert static asset files
make collectstatic

# Apply any outstanding database migrations
make migrate