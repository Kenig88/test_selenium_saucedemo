from tests.base_test import BaseTest
from data.login_data import Login
from data.login_data import Password
from time import sleep
import allure


@allure.feature("E2E test.")
class TestE2e(BaseTest):

    def test_checkout_flow(self, browser_fixture):

        # login_page
        self.login_page.open()
        self.login_page.is_opened_login_page()
        sleep(1)
        self.login_page.login(username=Login.STANDARD_USER, password=Password.SECRET_SAUCE)
        sleep(1)

        # products_page



