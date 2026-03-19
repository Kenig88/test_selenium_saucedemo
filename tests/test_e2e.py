from tests.base_test import BaseTest
from data.login_data import Login
from data.login_data import Password
from time import sleep
import allure
import pytest


@allure.feature("E2E test.")
@pytest.mark.e2e
class TestE2e(BaseTest):

    def test_checkout_flow(self):

        # login_page

        self.login_page.open()
        self.login_page.is_opened()
        sleep(1)
        self.login_page.login(username=Login.STANDARD_USER, password=Password.SECRET_SAUCE)
        sleep(1)

        # products_page

        title = self.products_page.is_opened()
        assert title == "Products"
        sleep(1)



