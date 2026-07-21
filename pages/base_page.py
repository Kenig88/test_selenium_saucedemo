import logging
from typing import Tuple

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = Tuple[str, str]

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, url: str, timeout: int = 10):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, timeout)


    # --- Navigation (навигация по страницам) ---

    def open(self) -> None:
        """
        Открыть страницу по URL, заданному в Page Object.
        Используется для стартовой страницы (LoginPage).
        """
        logger.info("Open page: %s", self.url)
        self.driver.get(self.url)


    # --- Page state (проверка состояния страницы) ---

    def assert_page_opened(self, url_part: str, title_locator: Locator) -> str:
        """
        Проверяю, что открыта нужная страница:
        - URL содержит ожидаемую часть
        - ключевой элемент (заголовок) видим

        Метод возвращает текст заголовка.
        """
        logger.info("Check that page is opened. Expected URL part: %s", url_part)

        element = self.find(title_locator)
        current_url = self.driver.current_url

        logger.debug("Current URL: %s", current_url)

        assert url_part in current_url, f"Ожидал '{url_part}' в URL, получил '{current_url}'."

        logger.info("Page opened successfully. Title text: %s", element.text)
        return element.text


    # --- Find elements (поиск элементов) ---

    def find(self, locator: Locator):
        """
        Найти один элемент с ожиданием (visibility).
        Основной метод для работы с элементами.
        """
        logger.debug("Find visible element: %s", locator)
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator):
        """
        Найти список элементов без ожидания.
        Используется, когда элемент может отсутствовать.
        """
        logger.debug("Find all elements: %s", locator)
        return self.driver.find_elements(*locator)

    def wait_for_element_absent(self, locator: Locator) -> None:
        """Дождаться исчезновения элемента из DOM или его невидимости."""
        logger.debug("Wait for element to disappear: %s", locator)
        self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_for_elements_count(self, locator: Locator, expected_count: int) -> None:
        """Дождаться ожидаемого количества элементов."""
        logger.debug("Wait for %s elements: %s", expected_count, locator)
        self.wait.until(
            lambda driver: len(driver.find_elements(*locator)) == expected_count
        )


    # --- Actions (действия пользователя) ---

    def click(self, locator: Locator) -> None:
        """
        Клик по элементу с ожиданием, что он кликабельный.
        """
        logger.info("Click element: %s", locator)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: Locator, text: str, clear: bool = True) -> None:
        """
        Ввод текста в поле:
        - по умолчанию очищает поле перед вводом
        - можно отключить очистку (clear=False)
        """
        logger.info("Enter text into element: %s", locator)

        element = self.find(locator)

        if clear:
            logger.debug("Clear element before typing: %s", locator)
            element.clear()

        element.send_keys(text)


    # --- Get config (получение данных из UI) ---

    def get_text(self, locator: Locator) -> str:
        """
        Получить текст элемента.
        """
        logger.debug("Get text from element: %s", locator)
        return self.find(locator).text

    def get_elements_count(self, locator: Locator) -> int:
        """
        Получить количество элементов (например, товаров на странице).
        """
        logger.debug("Get elements count: %s", locator)
        return len(self.find_all(locator))