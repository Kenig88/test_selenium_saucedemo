# <p align="center"> SauceDemo UI Test Automation</p>

UI-проект автоматизации тестирования интернет-магазина [SauceDemo](https://www.saucedemo.com/).

Фреймворк построен на Python, Pytest и Selenium WebDriver, использует Page Object Model, поддерживает параллельный запуск, Docker, Allure Report и ручной запуск наборов тестов через GitHub Actions.

---

## <p align="center">Технологии</p>

- Python 3.11
- Pytest
- Selenium WebDriver
- Pytest-xdist
- Allure Pytest
- Docker и Docker Compose
- GitHub Actions
- GitHub Pages

---

## <p align="center">Что покрывает проект</p>

- успешная и неуспешная авторизация;
- валидация обязательных полей;
- отображение и сортировка товаров;
- переход на страницу деталей товара;
- добавление и удаление товара;
- работа с корзиной;
- checkout flow;
- успешное завершение заказа;
- два полных E2E-сценария оформления заказа.

На момент подготовки проекта Pytest собирает **25 тестов**.

---

## <p align="center">Архитектура</p>

Проект использует Page Object Model:

- `pages/` содержит локаторы и действия со страницами;
- `tests/` содержит проверки пользовательских сценариев;
- `config/` содержит тестовые данные, URL и тексты ошибок;
- `conftest.py` отвечает за WebDriver, Page Object fixtures и подготовку состояний;
- Allure-разметка находится на уровне тестов и пользовательских шагов.

```text
saucedemo_test_ui/
├── .github/
│   └── workflows/
│       └── ui-tests.yml
├── config/
│   ├── checkout_data.py
│   ├── links.py
│   ├── login_data.py
│   └── products_data.py
├── pages/
│   ├── base_page.py
│   ├── cart_page.py
│   ├── checkout_complete_page.py
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   ├── login_page.py
│   ├── product_details_page.py
│   └── products_page.py
├── tests/
│   ├── e2e/
│   ├── test_cart_page.py
│   ├── test_checkout_complete_page.py
│   ├── test_checkout_info_page.py
│   ├── test_checkout_overview_page.py
│   ├── test_login_page.py
│   └── test_products_page.py
├── conftest.py
├── pytest.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## <p align="center">Переменные окружения</p>

Создай `.env` на основе `.env.example`:

```dotenv
BASE_URL=https://www.saucedemo.com/

STANDARD_USER=standard_user
LOCKED_OUT_USER=locked_out_user
SECRET_SAUCE=your_password
INVALID_PASSWORD=invalid_password
```

Обязательные значения проверяются при загрузке тестовых данных. Если переменная отсутствует, запуск завершится с понятной ошибкой.

`BASE_URL` необязателен: по умолчанию используется `https://www.saucedemo.com/`.

Файл `.env` исключён из Git через `.gitignore`.

---

## <p align="center">Установка и локальный запуск</p>

Создание виртуального окружения:

```bash
python -m venv .venv
```

Активация в Windows:

```bash
.venv\Scripts\activate
```

Активация в Linux или macOS:

```bash
source .venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Запуск всех тестов:

```bash
pytest
```

Параллельный запуск:

```bash
pytest -n 2
```

Запуск отдельного файла:

```bash
pytest tests/test_login_page.py
```

Тесты запускают Chrome в headless-режиме. Локально Selenium использует установленный ChromeDriver или Selenium Manager. В Docker пути к Chromium и ChromeDriver передаются через переменные окружения.

---

## <p align="center">Маркеры тестов</p>

| Маркер | Назначение |
|---|---|
| `smoke` | Критические проверки основного пользовательского пути |
| `regression` | Полный регрессионный набор |
| `negative` | Проверки валидации и ошибочных сценариев |
| `e2e` | Полные пользовательские цепочки оформления заказа |

Запуск наборов локально:

```bash
pytest -m smoke
pytest -m regression
pytest -m negative
pytest -m e2e
```

Маркеры могут пересекаться. Например, основной E2E-сценарий одновременно входит в `e2e`, `regression` и `smoke`.

---

## <p align="center">Запуск через Docker</p>

Сборка образа:

```bash
docker compose build
```

Запуск всех тестов:

```bash
docker compose run --rm all
```

Запуск отдельных наборов тестов через одноимённые Docker Compose-сервисы:

```bash
docker compose run --rm smoke
docker compose run --rm regression
docker compose run --rm negative
docker compose run --rm e2e
```

Количество параллельных worker-процессов можно задать через `.env` или при запуске:

```bash
PYTEST_WORKERS=4 docker compose run --rm all
```

Для Windows PowerShell:

```powershell
$env:PYTEST_WORKERS=4
docker compose run --rm all
```

---

## <p align="center">Allure Report</p>

Создание результатов:

```bash
pytest --alluredir=allure-results --clean-alluredir
```

Просмотр интерактивного отчёта:

```bash
allure serve allure-results
```

Создание статического отчёта:

```bash
allure generate allure-results -o allure-report --clean
```

При падении теста `conftest.py` пытается сделать скриншот браузера и прикрепить его к Allure. Ошибка при создании скриншота не заменяет исходную ошибку теста.

---

## <p align="center">Логирование</p>

Pytest выводит логи в терминал и сохраняет их в:

```text
logs/ui-tests.log
```

Папка `logs/` создаётся перед Docker-запуском и исключена из Git.

---

## <p align="center">GitHub Actions CI</p>

Workflow расположен в:

```text
.github/workflows/ui-tests.yml
```

Запуск выполняется вручную через вкладку **Actions**. Перед стартом можно выбрать:

- `all`;
- `smoke`;
- `regression`;
- `negative`;
- `e2e`;
- количество worker-процессов Pytest-xdist.

В GitHub необходимо создать Repository Secrets:

```text
STANDARD_USER
LOCKED_OUT_USER
SECRET_SAUCE
INVALID_PASSWORD
```

Workflow:

1. собирает Docker-образ;
2. запускает выбранный набор тестов;
3. сохраняет `allure-results` и логи как artifacts;
4. восстанавливает историю предыдущих Allure-запусков;
5. генерирует отчёт;
6. публикует его в ветку `gh-pages`;
7. возвращает ошибочный статус, если тесты не прошли.

Онлайн-отчёт проекта:

```text
https://kenig88.github.io/saucedemo_test_ui/
```

История запусков доступна в Allure:

```text
Graphs → Trend
```

---

## <p align="center">Надёжность тестов</p>

В проекте используются:

- явные ожидания Selenium вместо `time.sleep()`;
- отдельный WebDriver для каждого теста;
- гарантированное закрытие браузера через `try/finally`;
- ожидание обновления корзины после добавления и удаления товара;
- ожидание удаления товара из DOM;
- ожидание изменения списка цен после сортировки;
- скриншот при падении теста;
- параллельный запуск через Pytest-xdist.

---

## <p align="center">Что демонстрирует проект</p>

- построение UI test automation framework;
- Page Object Model;
- работу с Selenium WebDriver и явными ожиданиями;
- управление тестовыми состояниями через Pytest fixtures;
- позитивные, негативные, smoke, regression и E2E-проверки;
- Allure-отчётность;
- контейнерный запуск;
- CI/CD-интеграцию и публикацию отчётов в GitHub Pages.
