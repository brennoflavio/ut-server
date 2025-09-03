from crontab import CronTab
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.cron import CronJob

cron_router = APIRouter()


class CronJobModel(BaseModel):
    appid: str
    token: str
    cron_expression: str


class DeleteCronJobModel(BaseModel):
    appid: str
    token: str


@cron_router.post("/cron", status_code=201)
async def create_cron_job(cron_job: CronJobModel, session: AsyncSession = Depends(get_session)):
    try:
        cron = CronTab(cron_job.cron_expression)
        cron.next()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid cron expression")

    stmt = select(CronJob).where(CronJob.appid == cron_job.appid, CronJob.token == cron_job.token)
    result = await session.execute(stmt)
    existing_cron_job = result.scalar_one_or_none()

    if existing_cron_job:
        existing_cron_job.cron_expression = cron_job.cron_expression
        await session.commit()
        await session.refresh(existing_cron_job)
        return
    else:
        new_cron_job = CronJob(
            appid=cron_job.appid,
            token=cron_job.token,
            cron_expression=cron_job.cron_expression,
        )
        session.add(new_cron_job)
        await session.commit()
        await session.refresh(new_cron_job)
        return


@cron_router.delete("/cron", status_code=204)
async def delete_cron_job(cron_job: DeleteCronJobModel, session: AsyncSession = Depends(get_session)):
    stmt = select(CronJob).where(CronJob.appid == cron_job.appid, CronJob.token == cron_job.token)
    result = await session.execute(stmt)
    existing_cron_job = result.scalar_one_or_none()

    if not existing_cron_job:
        return

    await session.delete(existing_cron_job)
    await session.commit()
    return
