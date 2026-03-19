from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
import allure
from dotenv import load_dotenv

load_dotenv()
# Обычно load_dotenv() кладут не в data-файл, а в: 👉 conftest.py Так он выполняется один раз перед всеми тестами.


@pytest.fixture()
def browser_fixture():
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failed",
                attachment_type=allure.attachment_type.PNG
            )
