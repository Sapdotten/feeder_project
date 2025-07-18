import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from src.motor import MotorController
from src.gps import GpsController
from src.utils import get_yaml

from src import models
from src.configs import Config

CONFIG_PATH = '../config.yaml'  # Путь к файлу с настройками

motor: MotorController
gps: GpsController
lock: asyncio.Lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global motor, gps

    configs = get_yaml(CONFIG_PATH)
    motor = MotorController(**configs['motor'])
    gps = GpsController(**configs['gps'])

    motor.setup()
    gps.setup()

    yield

    motor.close()
    gps.close()


app = FastAPI(lifespan=lifespan)


@app.get("/whoami", response_model=models.MyResponseModel, status_code=200)
async def whoami() -> models.MyResponseModel:
    return models.MyResponseModel(id=Config().my_id)  # type: ignore


@app.post("/feed", response_model=models.FeedResponseModel, status_code=200)
async def feed(request: models.FeedRequestModel) -> models.FeedResponseModel:
    async with lock:
        await asyncio.to_thread(motor.rotate, request.food_amount)
    return models.FeedResponseModel(status="Success")


@app.get("gps", response_model=models.MyGps, status_code=200)
async def get_gps() -> models.MyGps:
    async with lock:
        raw = await asyncio.to_thread(gps.read_data)
    coords = GpsController.parse_coords(raw)
    if coords:
        return models.MyGps(latitude=coords[0], longitude=coords[1])
    else:
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить координаты с GPS-модуля"
        )
