import time
import serial
import yaml

serialPort: serial.Serial


def setup():
    # чтение конфигурации
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    uart_port = config['gps']['uart_port']
    baud_rate = config['gps']['baud_rate']
    # открытие порта для GPS-модуля
    global serialPort
    serialPort = serial.Serial(uart_port, baud_rate, timeout=1)


def close():
    serialPort.close()


def read_data() -> str:
    data = ''
    while not data.startswith('$GPGGA'):  # Проверяем, есть ли нужные данные
        if serialPort.in_waiting > 0:  # Проверяем, есть ли данные для чтения
            data = serialPort.readline().decode('utf-8', errors='ignore').rstrip()  # Читаем строку и декодируем
        time.sleep(0.1)
    return data


if __name__ == "__main__":
    setup()
    try:
        while True:
            data = read_data()
            print(data)
            time.sleep(1)
    except KeyboardInterrupt:
        close()
