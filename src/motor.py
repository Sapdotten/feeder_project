import time
from OPi import GPIO
import pi3b
import yaml

# Конфигурация вращения
direction: bool  # направление вращения вала
step_division: float  # Деление шага, заданное на драйвере
rotation_count: int  # Количество оборотов при вращении вала
step_delay: float  # Задержка между шагами вращения (скорость вращения) в секундах
steps: int  # Количество шагов для одного цикла вращения

# Конфигурация подключения
direction_pin: int  # Пин направления вращения
step_pin: int  # Пин активации шага
enable_pin: int  # Пин включения питания двигателя


def setup():
    with open('../config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    # Конфигурация вращения
    global step_division
    step_division = config['motor']['step_division']
    global rotation_count
    rotation_count = config['motor']['rotation_count']
    global step_delay
    step_delay = config['motor']['step_delay']
    global direction
    direction = config['motor']['direction']
    global steps
    steps = int(200 / step_division * rotation_count)

    # Конфигурация подключения
    global direction_pin
    direction_pin = config['motor']['direction_pin']
    global step_pin
    step_pin = config['motor']['step_pin']
    global enable_pin
    enable_pin = config['motor']['enable_pin']

    GPIO.setmode(pi3b.BOARD)
    # Установка нумерации пинов по схеме
    GPIO.setup(step_pin, GPIO.OUT)
    GPIO.setup(direction_pin, GPIO.OUT)
    GPIO.setup(enable_pin, GPIO.OUT)

    GPIO.output(direction_pin, GPIO.HIGH if direction else GPIO.LOW)  # Устанавливаем направление вращения


def close():
    # Отключение двигателя при завершении программы
    GPIO.output(enable_pin, GPIO.HIGH)  # HIGH
    GPIO.cleanup()


def rotate():
    GPIO.output(enable_pin, GPIO.LOW)  # Включаем двигатель
    for x in range(steps):
        GPIO.output(step_pin, GPIO.HIGH)  # Активируем шаг
        time.sleep(step_delay)  # Задержка в миллисекундах
        GPIO.output(step_pin, GPIO.LOW)  # Деактивируем шаг
        time.sleep(step_delay)  # Задержка в миллисекундах
    GPIO.output(enable_pin, GPIO.HIGH)  # Отключаем двигатель
    time.sleep(1)  # Ждем секунду


if __name__ == "__main__":
    setup()
    try:
        while True:
            rotate()
    except KeyboardInterrupt:
        close()
