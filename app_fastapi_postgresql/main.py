from fastapi import FastAPI

from app_fastapi_postgresql import models
from app_fastapi_postgresql.database import engine

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome"}

models.Base.metadata.create_all(bind=engine)
