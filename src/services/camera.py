import subprocess
import time

from pydantic import BaseModel, ConfigDict

from src.configs import Config
from src.utils import get_yaml


class CameraController(BaseModel):
    resolution: str
    max_fps: int
    config: Config = Config()  # type: ignore
    process: subprocess.Popen | None = None
    is_running: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow"
    )

    def setup(self):
        rtsp_host = self.config.rtsp_host
        rtsp_port = self.config.rtsp_port
        rtsp_suffix = self.config.rtsp_suffix

        command = [
            'ffmpeg',
            '-f', 'v4l2',
            '-i', '/dev/video3',
            '-vf', 'format=yuv420p',
            '-s', self.resolution,
            '-r', str(self.max_fps),
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-threads', '4',
            '-f', 'rtsp',
            f'rtsp://{rtsp_host}:{rtsp_port}/{rtsp_suffix}'
        ]
        self.process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.is_running = True
        print(f'Запущен процесс ffmpeg с PID: {self.process.pid}')

    def close(self):
        if self.process:
            self.process.terminate()  # Завершаем процесс корректно
            self.process.wait()  # Ждем завершения процесса
            print("Процесс ffmpeg завершен.")
            self.is_running = False


if __name__ == "__main__":

    camera = CameraController(**get_yaml('../config.yaml')['camera'])
    camera.setup()
    time.sleep(60)
    camera.close()
