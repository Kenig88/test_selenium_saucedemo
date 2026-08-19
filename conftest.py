import logging
import os
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.checkout_data import CheckoutInfoData
from config.login_data import Password, Username
from config.products_data import ProductNames
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent
LOGS_DIR = PROJECT_ROOT / "logs"


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Создаёт отдельный лог для каждого xdist worker."""
    LOGS_DIR.mkdir(exist_ok=True)
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "main")
    config.option.log_file = str(LOGS_DIR / f"ui-tests-{worker_id}.log")

    # Selenium DEBUG-логи содержат payload команды send_keys, включая пароль.
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# Прикрепляет скриншот к Allure при падении теста
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        driver = item.funcargs.get("browser_fixture")
        if driver:
            worker_id = "main"
            if hasattr(item.config, "workerinput"):
                worker_id = item.config.workerinput.get("workerid", "worker")

            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"failed-{report.when}-{worker_id}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception:
                logger.exception("Не удалось прикрепить скриншот к Allure")


# Создаёт и закрывает WebDriver для каждого теста
@pytest.fixture()
def browser_fixture():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--window-size=1920,1080")

    # Для Docker, CI и стабильной работы на Windows
    options.add_argument("--headless=new")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-allow-origins=*")

    chrome_bin = os.getenv("CHROME_BIN")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")

    if chrome_bin:
        options.binary_location = chrome_bin

    if chromedriver_path:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(20)

    try:
        yield driver
    finally:
        driver.quit()


# Возвращает PageObject страницы логина
@pytest.fixture()
def login_page(browser_fixture):
    return LoginPage(browser_fixture)


# Возвращает PageObject страницы товаров
@pytest.fixture()
def products_page(browser_fixture):
    return ProductsPage(browser_fixture)


# Возвращает PageObject страницы деталей товара
@pytest.fixture()
def product_details_page(browser_fixture):
    return ProductDetailsPage(browser_fixture)


# Возвращает PageObject страницы корзины
@pytest.fixture()
def cart_page(browser_fixture):
    return CartPage(browser_fixture)


# Возвращает PageObject страницы checkout (шаг 1)
@pytest.fixture()
def checkout_info_page(browser_fixture):
    return CheckoutInfoPage(browser_fixture)


# Возвращает PageObject страницы checkout (шаг 2)
@pytest.fixture()
def checkout_overview_page(browser_fixture):
    return CheckoutOverviewPage(browser_fixture)


# Возвращает PageObject страницы успешного завершения заказа
@pytest.fixture()
def checkout_complete_page(browser_fixture):
    return CheckoutCompletePage(browser_fixture)


# =========================
# Фикстуры действий
# =========================


# Выполняет логин пользователя
@pytest.fixture()
def logged_in_products_page(login_page, products_page):
    login_page.open()
    login_page.user_input(
        username=Username.STANDARD_USER, password=Password.SECRET_SAUCE
    )
    return products_page


# Открывает корзину с добавленным товаром
@pytest.fixture()
def cart_page_with_product(logged_in_products_page, cart_page):
    def _open(product_name):
        logged_in_products_page.add_to_cart(product_name)
        logged_in_products_page.click_open_cart()
        return cart_page

    return _open


# Открывает checkout step one после добавления товара в корзину
@pytest.fixture()
def opened_checkout_info_page(logged_in_products_page, cart_page, checkout_info_page):
    logged_in_products_page.add_to_cart(ProductNames.BACKPACK)
    logged_in_products_page.click_open_cart()
    cart_page.click_checkout()
    return checkout_info_page


# Открывает checkout overview после заполнения данных
@pytest.fixture()
def opened_checkout_overview_page(opened_checkout_info_page, checkout_overview_page):
    opened_checkout_info_page.enter_checkout_form(
        first_name=CheckoutInfoData.FIRST_NAME,
        last_name=CheckoutInfoData.LAST_NAME,
        postal_code=CheckoutInfoData.POSTAL_CODE,
    )
    opened_checkout_info_page.click_continue_button()
    return checkout_overview_page


# Открывает страницу успешного завершения заказа
@pytest.fixture()
def opened_checkout_complete_page(
    opened_checkout_overview_page, checkout_complete_page
):
    opened_checkout_overview_page.click_finish()
    return checkout_complete_page