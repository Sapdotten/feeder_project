from pydantic import BaseModel
from enum import Enum


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
