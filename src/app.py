from fastapi import FastAPI, Request
from src import models
from src.configs import Config
from src.service import Service
import asyncio

app = FastAPI()


@app.get("/whoami", response_model=models.MyResponseModel, status_code=200)
async def whoami() -> models.MyResponseModel:
    return models.MyResponseModel(id=Config().my_id)  # type: ignore


@app.post("/feed", response_model=models.FeedResponseModel, status_code=200)
async def feed(request: models.FeedRequestModel) -> models.FeedResponseModel:
    async with Service.lock:
        await asyncio.to_thread(Service.feed, request.food_amount)
    return models.FeedResponseModel(status="Success")
