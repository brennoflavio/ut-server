from fastapi import FastAPI

from endpoints.crash import crash_router

app = FastAPI()
app.include_router(crash_router, prefix="")
