from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from data.links import Links


class ProductDetailsPage(BasePage):
    TITLE = (By.CLASS_NAME, "inventory_details_name")

    def __init__(self, driver):
        super().__init__(driver, url=Links.PRODUCTS_DETAILS_PAGE)

    def is_opened(self) -> bool:
        return Links.PRODUCTS_DETAILS_PAGE in self.driver.current_url

    def get_product_title(self) -> str:
        return self.get_text(self.TITLE)
