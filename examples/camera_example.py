from src.utils import get_yaml
from src.services.camera import CameraController
import time
import sys
from pathlib import Path

# добавляем src/ в sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


if __name__ == '__main__':
    camera = CameraController(**get_yaml('./config.yaml')['camera'])
    camera.setup()
    time.sleep(60)
    camera.close()
