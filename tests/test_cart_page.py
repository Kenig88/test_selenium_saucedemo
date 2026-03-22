import pytest
import allure


@allure.feature("Cart Page")
@pytest.mark.regression
class TestCartPage:

    @allure.story("Отображение товара в корзине")
    @allure.title("Пользователь видит добавленный товар в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("product_name", [
        "Sauce Labs Backpack",  # популярный товар
        "Test.allTheThings() T-Shirt (Red)",  # edge-case название
    ])
    def test_user_sees_added_product_in_cart(self, login, products_page, cart_page, product_name):
        allure.dynamic.parameter("Товар", product_name)
        assert products_page.is_opened() == "Products"
        products_page.add_to_cart(product_name)
        products_page.click_open_cart()
        assert cart_page.is_opened() == "Your Cart"
        assert cart_page.is_product_in_cart(product_name), \
            f"Товар '{product_name}' не найден в корзине"

    @allure.story("Удаление товара")
    @allure.title("Пользователь может удалить товар из корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("product_name", [
        "Sauce Labs Backpack",
        "Test.allTheThings() T-Shirt (Red)",
    ])
    def test_user_can_remove_product_from_cart(self, login, products_page, cart_page, product_name):
        allure.dynamic.parameter("Товар", product_name)
        assert products_page.is_opened() == "Products"
        products_page.add_to_cart(product_name)
        products_page.click_open_cart()
        assert cart_page.is_opened() == "Your Cart"
        assert cart_page.is_product_in_cart(product_name), \
            "Товар не появился в корзине перед удалением"
        cart_page.remove_from_cart(product_name)
        assert not cart_page.is_product_in_cart(product_name), \
            f"Товар '{product_name}' не был удалён из корзины"
        assert cart_page.get_products_count() == 0, \
            "После удаления корзина должна быть пустой"

    @allure.story("Переход в checkout")
    @allure.title("Пользователь может перейти к оформлению заказа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_can_go_to_checkout_from_cart(
            self,
            login,
            products_page,
            cart_page,
            checkout_info_page
    ):
        product_name = "Sauce Labs Bike Light"
        assert products_page.is_opened() == "Products"
        products_page.add_to_cart(product_name)
        products_page.click_open_cart()
        assert cart_page.is_opened() == "Your Cart"
        cart_page.click_checkout()
        assert "checkout-step-one" in checkout_info_page.driver.current_url, \
            f"Ожидался переход на checkout-step-one, получен {checkout_info_page.driver.current_url}"

    @allure.story("Возврат к товарам")
    @allure.title("Пользователь может вернуться к списку товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_can_return_to_products_from_cart(self, login, products_page, cart_page):
        assert products_page.is_opened() == "Products"
        products_page.click_open_cart()
        assert cart_page.is_opened() == "Your Cart"
        cart_page.click_continue_shopping()
        assert "inventory" in products_page.driver.current_url, \
            f"Ожидался переход на inventory, получен {products_page.driver.current_url}"
