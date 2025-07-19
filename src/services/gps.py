import time
import serial
from pydantic import BaseModel, ConfigDict
from src.utils import get_yaml


class GpsController(BaseModel):
    uart_port: str
    baud_rate: int
    timeout: int = 1

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow"
    )

    def setup(self):
        self.serialPort = serial.Serial(
            self.uart_port,
            self.baud_rate,
            timeout=self.timeout
        )

    def close(self) -> None:
        self.serialPort.close()

    def read_data(self) -> str:
        data = ""
        # Проверяем, есть ли нужные данные
        while not data.startswith("$GPGGA"):
            time.sleep(0.1)
            if self.serialPort.in_waiting > 0:  # Проверяем, есть ли данные для чтения
                data = (  # Проверяем, есть ли нужные данные
                    self.serialPort.readline().decode("utf-8", errors="ignore").rstrip()
                )

        return data

    @staticmethod
    def parse_coords(source: str) -> tuple[str, str] | None:
        if not source:
            return None
        coords = source.split(',')
        for i in range(2, 5):
            if coords[i+1] in 'SW':
                coords[i] = '-' + coords[i]
        return coords[2], coords[4]


if __name__ == "__main__":
    gps = GpsController(**get_yaml("../config.yaml")['gps'])
    gps.setup()
    try:
        while True:
            data = gps.read_data()
            print(data)
            time.sleep(1)
    except KeyboardInterrupt:
        gps.close()
