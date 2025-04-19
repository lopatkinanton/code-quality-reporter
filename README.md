# Сode Quality Reporter

Инструмент для анализа качества кода разработчиков. 

Решение кейса АльфаСтрахования в хакатоне LLM Coding Challenge от команды Cornmasters.

## Установка

1. Клонируйте репозиторий:

```
git clone https://github.com/lopatkinanton/code-quality-reporter.git
cd code-quality-reporter
```

2. (Необязательно) Создайте и активируйте виртуальное окружение:

```
python -m venv venv
venv\Scripts\activate     # для Windows
```

```
python -m venv venv
source venv/bin/activate  # для Linux/macOS
```

3. Установите зависимости:

```
pip install -r requirements.txt
```

4. Переменные окружения

Перед запуском проекта необходимо задать некоторые переменные окружения. 

Создайте файл .env в корне проекта и укажите в нём следующие переменные:

GITHUB_TOKEN - для доступа к GitHub API
OPENAI_API_KEY - для доступа к OpenAI API
OPENAI_API_BASE - (если используется кастомный эндпоинт)

## Запуск

```
python main.py --repo REPO --author AUTHOR --start-date START_DATE --end-date END_DATE

options:
  -h, --help            show this help message and exit
  --repo REPO           Repository name, e.g., 'user/repo'
  --author AUTHOR       Author email
  --start-date START_DATE
                        Start date in YYYY-MM-DD format
  --end-date END_DATE   End date in YYYY-MM-DD format
  --output-dir OUTPUT_DIR
                        Output directory (default: ./output)
```