import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db
from endpoints.crash import crash_router
from endpoints.cron import cron_router
from jobs.cron import run_cron_jobs


async def run_background_tasks():
    while True:
        try:
            await run_cron_jobs()
        except Exception as e:
            logging.error(f"Error in cron job: {e}")
        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    task = asyncio.create_task(run_background_tasks())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(lifespan=lifespan)
app.include_router(crash_router)
app.include_router(cron_router)
