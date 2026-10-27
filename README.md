# Text Utilities Service

[EN](README.md) | [RU](README.ru.md)

A lightweight text processing web service and API built with FastAPI and Jinja2.

## Project Tree
```
text-utilities
├── app_final.py
├── .env.example
├── .github
│   └── workflows
│       └── test.yml
├── .gitignore
├── LICENSE.txt
├── README.md
├── README.ru.md
├── requirements-dev.txt
├── requirements.txt
├── templates
│   ├── analyzer.html
│   ├── base.html
│   ├── case.html
│   ├── index.html
│   └── slugify.html
└── tests
    ├── test_api.py
    └── test_logic.py
```
## Requirements

Python 3.12 and newer.

## Quick Start

Clone this repository:
```bash
git clone https://github.com/futsaidl/text-utilities.git
cd text-utilities
```

Create a virtual environment and enter it:

```bash
python3 -m venv venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
uvicorn app_final:app --host 127.0.0.1 --port 8000
```
Launch your browser and navigate to `http://127.0.0.1` in your browser to try out different tools.
## Environment variables
Set up the following variables using the provided `.env.example` file or manually:

```bash
export APP_NAME="Text Utilities Service"
export APP_VERSION="1.0.0"
export DEFAULT_CASE_MODE="snake"
``` 
Available values for `DEFAULT_CASE_MODE`:
| Value | Description |
| :---- | ---------- |
| `"upper"` | UPPERCASE|
|`"lower"` | lowercase |
|`"snake"` | snake_case |
|`"camel"` | camelCase |
|`"pascal"` | PascalCase|
|`"alternating"` | aLtErNaTiNg CaSe |


## Routes


| Route | Method | Description |
| :-------- | :--------: | -------- |
| `/api/health`   | GET   | App status check   |
| `/api/version`   | GET   | App version   |
|`/api/analyze`|GET|Analyze text and return JSON|
|`/api/slugify`|GET|Return slug for the provided text. Non-diacritic Latin and Cyrillic are supported.|
|`/api/case`|GET|Convert the provided text into a chosen case mode|
|`/`|GET|HTML Jinja2 template for the main page|
|`/analyze`|GET|HTML Jinja2 template for the text analyzer|
|`/slugify`|GET|HTML Jinja2 template for the slug generator|
|`/case`|GET|HTML Jinja2 template for the case converter|

Swagger documentation is available at `http://127.0.0.1:8000/docs`.

## Usage
To use the API directly, use `curl`:

```bash
curl "http://127.0.0.1:8000/api/health"
curl "http://127.0.0.1:8000/api/version"
curl "http://127.0.0.1:8000/api/analyze?text=..."
curl "http://127.0.0.1:8000/api/slugify?text=..."
curl "http://127.0.0.1:8000/api/case?text=...&mode=..."
```
## Tests

Unit tests for the functions are available at `tests/test_logic.py`. API and template tests are located at `tests/test_api.py`.

To run the tests, install the dependencies for them, and then run `pytest`:

```bash
pip install -r requirements-dev.txt
python3 -m pytest -v
```
## Github Actions
GitHub Actions CI YAML file is located at `.github/workflows/test.yml`. It runs tests every time a new commit is pushed to the repository to ensure the app is ready for deployment. It also creates a new artifact on each run.
## Logs and troubleshooting

Each API call is logged to the terminal where `uvicorn` is running. Logs are not stored in a file.

In case you get errors, make sure you activated the virtual environment and pass valid strings to the API endpoints.

Refer to the details of errors like `400: Bad Request`.