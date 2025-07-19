from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.gps import GpsController
from src.utils import get_yaml
import time



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
