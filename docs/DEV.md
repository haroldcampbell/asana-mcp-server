# Development

## Setup
```bash
uv venv
uv pip install -r requirements.txt
```

## Run
```bash
ASANA_TOKEN_FILE=.secrets/asana.token uv run python -m src.server
```

## Tests
```bash
uv pip install pytest
uv run pytest
```
