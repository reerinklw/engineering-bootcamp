# Project Rules

## Python Environment
- Use the virtual environment at `./venv/` for all Python commands
- Python executables:
  - `./venv/bin/python`
  - `./venv/bin/pip`
  - `./venv/bin/streamlit`
  - `./venv/bin/pytest`
- Dependencies are managed in `requirements.txt`

## Development Commands
- Run calculator app: `./venv/bin/streamlit run apps/calculator/calculator_app.py --server.headless true`
- Run tests: `./venv/bin/pytest`
- Install dependencies: `./venv/bin/pip install -r requirements.txt`

## Docker
- Build app image: `docker build -t 02-git-cicd-sandbox-app:latest .`
- Run with docker-compose: `docker-compose up`
