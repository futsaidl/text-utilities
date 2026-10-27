# Text Utilities Service

[EN](README.md) | [RU](README.ru.md)

Легковесный веб-сервис и API для обработки текста, созданный с использованием FastAPI и Jinja2.

## Дерево проекта
```
text-utilities
├── app_final.py
├── .env.example
├── .github
│ └── workflows
│ └── test.yml
├── .gitignore
├── LICENSE.txt
├── README.md
├── README.ru.md
├── requirements-dev.txt
├── requirements.txt
├── templates
│ ├── analyzer.html
│ ├── base.html
│ ├── case.html
│ ├── index.html
│ └── slugify.html
└── tests
├── test_api.py
└── test_logic.py
```
## Требования

Python 3.12 и новее.

## Быстрый старт

Клонируйте этот репозиторий:
```bash
git clone https://github.com/futsaidl/text-utilities.git
cd text-utilities
```

Создайте виртуальное окружение и войдите в него:

```bash
python3 -m venv venv
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Запустите приложение:

```bash
uvicorn app_final:app --host 127.0.0.1 --port 8000
```
Запустите браузер и перейдите по адресу `http://127.0.0.1`, чтобы попробовать различные инструменты.

## Переменные среды
Настройте следующие переменные, используя предоставленный файл `.env.example` или вручную:

```bash
export APP_NAME="Text Utilities Service"
export APP_VERSION="1.0.0"
export DEFAULT_CASE_MODE="snake"
```
Доступные значения для `DEFAULT_CASE_MODE`:

| Значение | Описание |
|:---|:---|
| `"upper"` | UPPERCASE |
| `"lower"` | lowercase |
| `"snake"` | snake_case |
| `"camel"` | camelCase |
| `"pascal"` | PascalCase |
| `"alternating"` | aLtErNaTiNg CaSe |

## Маршруты

| Маршрут | Метод | Описание |
| :-------- | :--------: | -------- |
| `/api/health` | GET | Проверка статуса приложения |
| `/api/version` | GET | Версия приложения |
|`/api/analyze`|GET|Анализ текста и возврат JSON|
|`/api/slugify`|GET|Возвращает слаг для предоставленного текста. Поддерживаются недиакритические латинские и кириллические символы.|
|`/api/case`|GET|Преобразует предоставленный текст в выбранный регистр|
|`/`|GET|HTML-шаблон Jinja2 для главной страницы|
|`/analyze`|GET|HTML-шаблон Jinja2 для текстового анализатора|
|`/slugify`|GET|HTML-шаблон Jinja2 для генератора слагов|
|`/case`|GET|HTML-шаблон Jinja2 для конвертера регистра|

Документация Swagger доступна по адресу `http://127.0.0.1:8000/docs`.

## Использование
Для прямого использования API используйте `curl`:

```bash
curl "http://127.0.0.1:8000/api/health"
curl "http://127.0.0.1:8000/api/version"
curl "http://127.0.0.1:8000/api/analyze?text=..."
curl "http://127.0.0.1:8000/api/slugify?text=..."
curl "http://127.0.0.1:8000/api/case?text=...&mode=..."
```
## Тесты

Модульные тесты для функций доступны в `tests/test_logic.py`. Тесты API и шаблонов находятся в `tests/test_api.py`.

Чтобы запустить тесты, установите для них зависимости, а затем запустите `pytest`:

```bash
pip install -r requirements-dev.txt
python3 -m pytest -v
```
## Github Actions
YAML-файл GitHub Actions CI находится по адресу `.github/workflows/test.yml`. Он запускает тесты каждый раз, когда в репозиторий отправляется новый коммит, чтобы убедиться, что приложение готово к развертыванию. При каждом запуске также создается новый артефакт.

## Логи и устранение неполадок

Каждый вызов API отправляется в терминал, где запущен `uvicorn`. Логи не сохраняются в файл.

В случае возникновения ошибок убедитесь, что вы активировали виртуальное окружение и передаете корректные строки в эндпоинты API.

В случае появления ошибок вида `400: Bad Request`, смотрите их детали.