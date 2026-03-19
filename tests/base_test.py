from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage

import pytest


@pytest.mark.usefixtures("browser_fixture")
class BaseTest:
    login_page: LoginPage
    products_page: ProductsPage
    cart_page: CartPage
    checkout_info_page: CheckoutInfoPage
    checkout_overview_page: CheckoutOverviewPage
    checkout_complete_page: CheckoutCompletePage

    @pytest.fixture(autouse=True)
    def setup_pages(self, browser_fixture):
        self.login_page = LoginPage(browser_fixture)
        # self.products_page = ProductsPage(browser_fixture)
        # self.cart_page = CartPage(browser_fixture)
        # self.checkout_info_page = CheckoutInfoPage(browser_fixture)
        # self.checkout_overview_page = CheckoutOverviewPage(browser_fixture)
        # self.checkout_complete_page = CheckoutCompletePage(browser_fixture)
