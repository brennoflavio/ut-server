from fastapi import APIRouter
from pydantic import BaseModel

from utils.email import send_email
from utils.env import EMAIL_TO

crash_router = APIRouter()


class CrashModel(BaseModel):
    report: str


@crash_router.post("/crash", status_code=201)
async def post_crash(crash: CrashModel):
    await send_email(to=EMAIL_TO, subject="Crash Report", body=crash.report)
    return
