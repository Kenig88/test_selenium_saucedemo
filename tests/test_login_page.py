import allure
import pytest

from config.login_data import ErrorMessages, Password, Username


@allure.feature("Login")
@pytest.mark.regression
class TestLoginPage:
    @pytest.mark.smoke
    @allure.story("Успешный логин")
    @allure.title("Пользователь может войти с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_user_can_login_with_valid_credentials(self, login_page, products_page):
        login_page.open()
        login_page.user_input(Username.STANDARD_USER, Password.SECRET_SAUCE)
        assert products_page.is_opened() == "Products", (
            "Страница ProductsPage не открылась"
        )

    @pytest.mark.negative
    @allure.story("Валидация формы")
    @allure.title("Пользователь видит ошибки при пустых обязательных полях")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "case_name",
        ["empty-username", "empty-password"],
    )
    def test_user_sees_error_with_empty_fields(self, login_page, case_name):
        cases = {
            "empty-username": (
                None,
                Password.SECRET_SAUCE,
                ErrorMessages.EMPTY_USERNAME,
            ),
            "empty-password": (
                Username.STANDARD_USER,
                None,
                ErrorMessages.EMPTY_PASSWORD,
            ),
        }
        username, password, expected_error = cases[case_name]

        login_page.open()
        if username:
            login_page.enter_username(username)
        if password:
            login_page.enter_password(password)
        login_page.click_login_button()
        assert login_page.error_message_text() == expected_error

    @pytest.mark.negative
    @allure.story("Невалидный логин")
    @allure.title("Пользователь видит ошибку при неуспешной попытке входа")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize(
        "case_name",
        ["invalid-password", "locked-out-user"],
    )
    def test_user_sees_error_when_login_fails(self, login_page, case_name):
        cases = {
            "invalid-password": (
                Username.STANDARD_USER,
                Password.INVALID_PASSWORD,
                ErrorMessages.INCORRECT_DATA,
            ),
            "locked-out-user": (
                Username.LOCKED_OUT_USER,
                Password.SECRET_SAUCE,
                ErrorMessages.BLOCKED_USER,
            ),
        }
        username, password, expected_error = cases[case_name]

        login_page.open()
        login_page.user_input(username, password)
        assert login_page.error_message_text() == expected_error
