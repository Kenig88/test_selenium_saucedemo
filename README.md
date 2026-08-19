# SauceDemo UI Test Automation

UI-автотесты учебного сайта [SauceDemo](https://www.saucedemo.com/) на Python,
Pytest и Selenium. Проект использует Page Object, запускается локально или в
Docker и публикует Allure Report через GitHub Actions.

[![UI Tests](https://github.com/Kenig88/test_selenium_saucedemo/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/Kenig88/test_selenium_saucedemo/actions/workflows/ui-tests.yml)

## Что проверяется

- успешный и неуспешный логин;
- валидация обязательных полей;
- список товаров и сортировка по цене;
- добавление и удаление одного или нескольких товаров;
- корзина;
- оба шага checkout;
- завершение заказа;
- два сквозных E2E-сценария.

## Наборы тестов

В проекте 26 тестовых сценариев. Один тест может входить сразу в несколько
наборов.

| Suite | Маркер | Количество |
| --- | --- | ---: |
| Все тесты | без маркера | 26 |
| Smoke | `smoke` | 7 |
| Regression | `regression` | 24 |
| Negative | `negative` | 7 |
| E2E | `e2e` | 2 |

E2E-тесты вынесены в отдельный набор и не дублируются в regression. Основной
E2E-сценарий при этом входит в smoke.

## Стек

- Python 3.11
- Pytest
- Selenium WebDriver
- Allure Pytest
- pytest-xdist
- Docker и Docker Compose
- GitHub Actions
- GitHub Pages

## Структура

```text
test_selenium_saucedemo/
├── .github/workflows/ui-tests.yml
├── config/
│   ├── checkout_data.py
│   ├── links.py
│   ├── login_data.py
│   └── products_data.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── products_page.py
│   ├── product_details_page.py
│   ├── cart_page.py
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
├── tests/
│   ├── e2e/
│   └── test_*.py
├── conftest.py
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
└── requirements.txt
```

## Переменные окружения

Создайте локальный файл `.env` из шаблона:

```bash
cp .env.example .env
```

Заполните значения:

```dotenv
BASE_URL=https://www.saucedemo.com/
STANDARD_USER=...
LOCKED_OUT_USER=...
SECRET_SAUCE=...
INVALID_PASSWORD=...
```

`.env` исключён из Git. Не добавляйте реальные логины и пароли в тестовые
параметры, логи или репозиторий.

## Локальный запуск

Нужны Python 3.11+ и установленный Chrome или Chromium.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Для Windows PowerShell активация окружения:

```powershell
.venv\Scripts\Activate.ps1
```

Запуск отдельных наборов:

```bash
pytest -m smoke
pytest -m regression
pytest -m negative
pytest -m e2e
```

Параллельный запуск:

```bash
pytest -n 4
pytest -n auto
```

## Запуск в Docker

```bash
docker compose build
docker compose run --rm all
```

Другие наборы:

```bash
docker compose run --rm smoke
docker compose run --rm regression
docker compose run --rm negative
docker compose run --rm e2e
```

Изменить число workers можно без редактирования файлов:

```bash
docker compose run --rm -e PYTEST_WORKERS=4 regression
```

Chromium и ChromeDriver уже установлены внутри образа. Исходники, логи и
`allure-results` пробрасываются в рабочую директорию проекта.

## Allure Report локально

Для локального HTML-отчёта нужны Java и Allure CLI:

```bash
pytest --alluredir=allure-results --clean-alluredir
allure serve allure-results
```

При падении теста фреймворк прикрепляет скриншот к Allure, если WebDriver уже
создан. Имя вложения содержит фазу теста и номер worker.

## Логи

При обычном запуске создаётся:

```text
logs/ui-tests-main.log
```

При `pytest-xdist` каждый worker пишет отдельно:

```text
logs/ui-tests-gw0.log
logs/ui-tests-gw1.log
```

Это исключает перемешивание строк из параллельных тестов. DEBUG-логи Selenium и
urllib3 отключены, потому что они могут содержать payload команды ввода.

## GitHub Actions

Workflow запускается вручную на вкладке **Actions → UI Tests → Run workflow**.
Перед запуском можно выбрать suite и число workers.

Добавьте в **Settings → Secrets and variables → Actions**:

- `STANDARD_USER`
- `LOCKED_OUT_USER`
- `SECRET_SAUCE`
- `INVALID_PASSWORD`

В **Settings → Pages → Build and deployment** выберите:

```text
Source: GitHub Actions
```

Workflow:

1. собирает Docker-образ;
2. запускает выбранный suite;
3. сохраняет логи как artifact;
4. формирует обычный отчёт для history;
5. формирует одностраничный отчёт для GitHub Pages;
6. публикует отчёт официальным GitHub Pages deployment;
7. сохраняет тренды в отдельной ветке `allure-history`;
8. возвращает failed-статус, если тесты упали.

Актуальный отчёт:

<https://kenig88.github.io/test_selenium_saucedemo/>

На сайте всегда отображается последний завершённый запуск. История нужна только
для графика тренда и не смешивает тесты разных запусков в одном отчёте.

## Основные решения

- Page Object хранит локаторы и действия, тесты — проверки и сценарии.
- Явные ожидания используются вместо `sleep`.
- Счётчик корзины ожидает конкретное значение, поэтому корректно работает с
  несколькими товарами.
- Данные авторизации читаются только из окружения.
- В Allure-параметры передаются безопасные имена кейсов, а не credentials.
- Один WebDriver создаётся на один тест и всегда закрывается в fixture teardown.

Проект намеренно остаётся компактным: без Selenium Grid, повторных запусков,
browser matrix, видео и дополнительных инфраструктурных слоёв.
