from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from data.links import Links


class ProductsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, url=Links.PRODUCTS_PAGE)

    # локаторы
    TITLE_PAGE = (By.XPATH, "//span[text()='Products']")
    SIDEBAR_BUTTON = (By.ID, "react-burger-menu-btn")
    CART_ICON_BUTTON = (By.ID, "shopping_cart_container")


    def is_opened(self) -> str:
        return self.assert_page_opened("inventory", self.TITLE_PAGE)
