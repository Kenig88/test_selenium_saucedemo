from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config.links import Links
from pages.base_page import BasePage


class ProductsPage(BasePage):
    TITLE = (By.XPATH, "//span[text()='Products']")
    CART = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    PRODUCT = (By.CLASS_NAME, "inventory_item")
    PRICE = (By.CLASS_NAME, "inventory_item_price")
    SORT = (By.CLASS_NAME, "product_sort_container")

    def __init__(self, driver):
        super().__init__(driver, url=Links.PRODUCTS_PAGE)

    def is_opened(self) -> str:
        return self.assert_page_opened("inventory.html", self.TITLE)

    def add_to_cart(self, product_name: str) -> None:
        previous_count = self.get_cart_count()
        locator = (
            By.XPATH,
            (
                f"//div[contains(@class, 'inventory_item')]"
                f"[.//*[contains(@class, 'inventory_item_name') and normalize-space()='{product_name}']]"
                f"//button[normalize-space()='Add to cart']"
            ),
        )
        self.click(locator)
        self.wait_for_cart_count(previous_count + 1)

    def remove_from_cart(self, product_name: str) -> None:
        previous_count = self.get_cart_count()
        locator = (
            By.XPATH,
            (
                f"//div[contains(@class, 'inventory_item')]"
                f"[.//*[contains(@class, 'inventory_item_name') and normalize-space()='{product_name}']]"
                f"//button[normalize-space()='Remove']"
            ),
        )
        self.click(locator)
        self.wait_for_cart_count(max(previous_count - 1, 0))

    def open_product_details(self, product_name: str) -> None:
        locator = (
            By.XPATH,
            f"//*[contains(@class, 'inventory_item_name') and normalize-space()='{product_name}']",
        )
        self.click(locator)

    def click_open_cart(self) -> None:
        self.click(self.CART)

    def sort_by(self, value: str) -> None:
        prices_before_sort = self.get_prices()
        Select(self.find(self.SORT)).select_by_value(value)
        self.wait.until(lambda _: self.get_prices() != prices_before_sort)

    def get_products_count(self) -> int:
        return self.get_elements_count(self.PRODUCT)

    def get_cart_count(self) -> int:
        badges = self.find_all(self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def wait_for_cart_count(self, expected_count: int) -> None:
        self.wait.until(lambda _: self.get_cart_count() == expected_count)

    def get_prices(self) -> list[float]:
        return [
            float(price.text.replace("$", "")) for price in self.find_all(self.PRICE)
        ]
