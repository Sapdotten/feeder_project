import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.motor import MotorController
from src.utils import get_yaml

from src import models
from src.configs import Config

motor: MotorController = MotorController(**get_yaml("./config.yaml")['motor'])
lock: asyncio.Lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    motor.setup()
    yield
    motor.close()


app = FastAPI(lifespan=lifespan)


@app.get("/whoami", response_model=models.MyResponseModel, status_code=200)
async def whoami() -> models.MyResponseModel:
    return models.MyResponseModel(id=Config().my_id)  # type: ignore


@app.post("/feed", response_model=models.FeedResponseModel, status_code=200)
async def feed(request: models.FeedRequestModel) -> models.FeedResponseModel:
    global lock
    async with lock:
        await asyncio.to_thread(motor.rotate, request.food_amount)
    return models.FeedResponseModel(status="Success")
