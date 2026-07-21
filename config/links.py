import os

from dotenv import load_dotenv

load_dotenv()


class Links:
    HOST = os.getenv("BASE_URL", "https://www.saucedemo.com/").rstrip("/") + "/"
    LOGIN_PAGE = HOST
    PRODUCTS_PAGE = f"{HOST}inventory.html"
    PRODUCTS_DETAILS_PAGE = f"{HOST}inventory-item.html?id="
    CART_PAGE = f"{HOST}cart.html"
    CHECKOUT_INFO_PAGE = f"{HOST}checkout-step-one.html"
    CHECKOUT_OVERVIEW_PAGE = f"{HOST}checkout-step-two.html"
    CHECKOUT_COMPLETE_PAGE = f"{HOST}checkout-complete.html"
