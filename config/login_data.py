import os

from dotenv import load_dotenv

load_dotenv()


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set")
    return value


class Username:
    STANDARD_USER = required_env("STANDARD_USER")
    LOCKED_OUT_USER = required_env("LOCKED_OUT_USER")


class Password:
    SECRET_SAUCE = required_env("SECRET_SAUCE")
    INVALID_PASSWORD = required_env("INVALID_PASSWORD")


class ErrorMessages:
    EMPTY_USERNAME = "Epic sadface: Username is required"
    EMPTY_PASSWORD = "Epic sadface: Password is required"
    INCORRECT_DATA = (
        "Epic sadface: Username and password do not match any user in this service"
    )
    BLOCKED_USER = "Epic sadface: Sorry, this user has been locked out."
