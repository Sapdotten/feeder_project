import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import time

from src.services.gps import GpsController
from src.utils import get_yaml

if __name__ == "__main__":
    gps = GpsController(**get_yaml("./config.yaml")['gps'])
    gps.setup()
    try:
        while True:
            data = gps.read_data()
            print(data)
            time.sleep(1)
    except KeyboardInterrupt:
        gps.close()
