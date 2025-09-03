from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


class CronJob(SQLModel, table=True):
    __tablename__ = "cron_job"  # type: ignore
    __table_args__ = (UniqueConstraint("appid", "token", name="unique_appid_token"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    appid: str = Field(nullable=False)
    token: str = Field(nullable=False)
    cron_expression: str = Field(nullable=False)
    next_run: int = Field(default=0, nullable=False)
