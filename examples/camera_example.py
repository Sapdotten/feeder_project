from pathlib import Path
import sys

# добавляем src/ в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.camera import Camera
from src.utils import get_yaml
import time




if __name__ == '__main__':
    camera = Camera(**get_yaml('./config.yaml')['camera'])
    camera.setup()
    time.sleep(60)
    camera.close()