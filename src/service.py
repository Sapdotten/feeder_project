from asyncio import Lock
from src.models import FoodAmount
from time import sleep


class Service:
    lock: Lock = Lock()

    @classmethod
    def feed(cls, food_amount: FoodAmount) -> None:
        print('Feeding process...')
        sleep(5)
        print("Cat fed succesefully")

