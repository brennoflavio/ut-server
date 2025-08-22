import os
from typing import Any, Callable, Optional


def get_env(env: str, convert_function: Optional[Callable[[str], Any]] = None, required: bool = False) -> Optional[Any]:
    value = os.getenv(env)
    if required and value is None:
        raise ValueError(f"Environment variable '{env}' is required")

    if not value:
        return None

    if convert_function:
        value = convert_function(value)

    return value


EMAIL_HOST = get_env("EMAIL_HOST", required=True)
EMAIL_PORT = get_env("EMAIL_PORT", convert_function=int, required=True)
EMAIL_START_TLS = get_env("EMAIL_START_TLS", convert_function=bool, required=True)
EMAIL_USERNAME = get_env("EMAIL_USERNAME", required=True)
EMAIL_PASSWORD = get_env("EMAIL_PASSWORD", required=True)
EMAIL_FROM = get_env("EMAIL_FROM", required=True)
EMAIL_TO = get_env("EMAIL_TO", required=True)
