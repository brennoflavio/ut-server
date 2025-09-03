import os
from typing import Any, Callable, Optional


def get_env(env: str, convert_function: Optional[Callable[[str], Any]] = None) -> Any:
    value = os.getenv(env)
    if value is None:
        raise ValueError(f"Environment variable '{env}' is required")

    if not value:
        return None

    if convert_function:
        value = convert_function(value)

    return value


EMAIL_HOST = get_env("EMAIL_HOST")
EMAIL_PORT = get_env("EMAIL_PORT", convert_function=int)
EMAIL_START_TLS = get_env("EMAIL_START_TLS", convert_function=bool)
EMAIL_USERNAME = get_env("EMAIL_USERNAME")
EMAIL_PASSWORD = get_env("EMAIL_PASSWORD")
EMAIL_FROM = get_env("EMAIL_FROM")
EMAIL_TO = get_env("EMAIL_TO")

DATABASE_URL = get_env("DATABASE_URL")
