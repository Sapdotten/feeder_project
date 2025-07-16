import time
from typing import Any

from OPi import GPIO
from pydantic import BaseModel

from src import pi3b
from src.models import FoodAmount


class MotorController(BaseModel):
    direction_pin: int
    step_pin: int
    enable_pin: int
    direction: bool
    rotation_count_small: int
    rotation_count_big: int
    step_division: float
    step_delay: float
    is_enabled: bool = False
    portion_steps: dict = {}

    def model_post_init(self, __context: Any) -> None:
        self.portion_steps = {
            FoodAmount.SMALL: int(200 / self.step_division * self.rotation_count_small),
            FoodAmount.BIG: int(200 / self.step_division * self.rotation_count_big),
        }
        self.is_enabled = False

    def setup(self) -> None:
        GPIO.setmode(pi3b.BOARD)
        # Установка нумерации пинов по схеме
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, GPIO.HIGH if self.direction else GPIO.LOW)
        self.is_enabled = True

    def close(self) -> None:
        # Отключение двигателя при завершении программы
        GPIO.output(self.enable_pin, GPIO.HIGH)  # HIGH
        GPIO.cleanup()

    def rotate(self, portion: FoodAmount) -> None:
        GPIO.output(self.enable_pin, GPIO.LOW)  # Включаем двигатель
        for _ in range(self.portion_steps[portion]):
            GPIO.output(self.step_pin, GPIO.HIGH)  # Активируем шаг
            time.sleep(self.step_delay)  # Задержка в миллисекундах
            GPIO.output(self.step_pin, GPIO.LOW)  # Деактивируем шаг
            time.sleep(self.step_delay)  # Задержка в миллисекундах
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Отключаем двигатель
        time.sleep(1)  # Ждем секунду


if __name__ == "__main__":
    from utils import get_yaml

    motor = MotorController(**get_yaml("../config.yaml"))
    motor.setup()
    try:
        while True:
            motor.rotate(FoodAmount.SMALL)
    except KeyboardInterrupt:
        motor.close()
