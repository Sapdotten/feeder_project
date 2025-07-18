from enum import Enum

from pydantic import BaseModel


class MyResponseModel(BaseModel):
    id: int


class LocationReposneModel(BaseModel):
    pass


class FoodAmount(int, Enum):
    SMALL = 0
    BIG = 0


class FeedRequestModel(BaseModel):
    food_amount: FoodAmount


class FeedResponseModel(BaseModel):
    status: str


class MyGps(BaseModel):
    latitude: str
    longitude: str
