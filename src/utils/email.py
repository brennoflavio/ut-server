from email.message import EmailMessage

import aiosmtplib

from utils.env import (
    EMAIL_FROM,
    EMAIL_HOST,
    EMAIL_PASSWORD,
    EMAIL_PORT,
    EMAIL_START_TLS,
    EMAIL_USERNAME,
)


async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = EMAIL_FROM
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=EMAIL_HOST,
        port=EMAIL_PORT,
        start_tls=EMAIL_START_TLS,
        username=EMAIL_USERNAME,
        password=EMAIL_PASSWORD,
    )
