import asyncio
import logging
import time
from datetime import datetime, timedelta

import httpx
from crontab import CronTab
from sqlalchemy import select

from database import async_session
from database.cron import CronJob


async def dispatch_notification(client: httpx.AsyncClient, appid: str, token: str):
    url = "https://push.ubports.com/notify"
    expire_at = datetime.utcnow() + timedelta(minutes=10)
    data = {
        "appid": appid,
        "expire_on": expire_at.isoformat() + "Z",
        "token": token,
        "data": {
            "notification": {
                "card": {
                    "icon": "notification",
                    "summary": "Cron Job",
                    "body": f"App {appid} just started a background job",
                    "popup": False,
                    "persist": False,
                },
                "vibrate": False,
                "sound": False,
            }
        },
    }

    response = await client.post(url, json=data)
    body = await response.aread()
    try:
        response.raise_for_status()
    except httpx.HTTPError as e:
        logging.error(
            f"Error dispatching notification. App {appid}, Response: {body.decode(errors='ignore')}, Error: {e}"
        )


async def run_cron_jobs():
    current_timestamp = int(time.time())

    async with async_session() as session:
        stmt = select(CronJob).where(CronJob.next_run <= current_timestamp)
        result = await session.execute(stmt)
        jobs = result.scalars().all()

        coroutines = []
        http_client = httpx.AsyncClient()
        for job in jobs:
            job.next_run = int(current_timestamp + int(CronTab(job.cron_expression).next(default_utc=True)))
            session.add(job)
            coroutines.append(dispatch_notification(http_client, job.appid, job.token))

        await asyncio.gather(*coroutines)
        await asyncio.gather(session.commit(), http_client.aclose())
        return jobs
