import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, status
from src.services.motor import MotorController
from src.services.gps import GpsController
from src.services.camera import CameraController
from src.utils import get_yaml

from src import models
from src.configs import Config

CONFIG_PATH = './config.yaml'  # Путь к файлу с настройками

motor: MotorController
gps: GpsController
camera: CameraController
lock: asyncio.Lock = asyncio.Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global motor, gps

    configs = get_yaml(CONFIG_PATH)
    motor = MotorController(**configs['motor'])
    gps = GpsController(**configs['gps'])
    camera = CameraController(**configs['camera'])

    camera.setup()
    motor.setup()
    gps.setup()

    yield

    camera.close()
    motor.close()
    gps.close()


app = FastAPI(lifespan=lifespan)


@app.get(
    "/whoami",
    response_model=models.MyResponseModel,
    status_code=200,
    tags=['device']
)
async def who_am_i() -> models.MyResponseModel:
    return models.MyResponseModel(id=Config().my_id)  # type: ignore


@app.post(
    "/feed",
    response_model=models.FeedResponseModel,
    status_code=200,
    tags=['feed']
)
async def feed(request: models.FeedRequestModel) -> models.FeedResponseModel:
    async with lock:
        await asyncio.to_thread(motor.rotate, request.food_amount)
    return models.FeedResponseModel(status=models.Status.success)


@app.get(
    "/gps",
    response_model=models.MyGps,
    status_code=200,
    tags=["device"]
)
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


@app.post(
    "/video/start",
    response_model=models.VideoResponse,
    tags=['video']
)
async def start_video() -> Response:
    if camera.is_running:
        return Response(
            content=models.VideoResponse(
                status=models.Status.unsuccess,
                text="Video already running"
            ).model_dump_json(),
            status_code=status.HTTP_208_ALREADY_REPORTED,
            media_type="application/json"
        )
    async with lock:
        await asyncio.to_thread(camera.setup)
    return Response(
        content=models.VideoResponse(
            status=models.Status.success,
            text="Video started"
        ).model_dump_json(),
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )


@app.post(
    "/video/stop",
    response_model=models.VideoResponse,
    tags=['video']
)
async def stop_video() -> Response:
    if not camera.is_running:
        return Response(
            content=models.VideoResponse(
                status=models.Status.unsuccess,
                text="Video already stopped"
            ).model_dump_json(),
            status_code=status.HTTP_208_ALREADY_REPORTED,
            media_type="application/json"
        )
    async with lock:
        await asyncio.to_thread(camera.close)
    return Response(
        content=models.VideoResponse(
            status=models.Status.success,
            text="Video started"
        ).model_dump_json(),
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )


@app.post(
    "/video/restart",
    response_model=models.VideoResponse,
    tags=['video']
)
async def restart_video() -> models.VideoResponse:
    async with lock:
        if camera.is_running:
            await asyncio.to_thread(camera.close)
        await asyncio.to_thread(camera.setup)
    return models.VideoResponse(
        status=models.Status.success,
        text="Video successfuly restarted"
    )
