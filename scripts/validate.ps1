$ErrorActionPreference = 'Stop'
python -m ruff check app tests
python -m pytest
