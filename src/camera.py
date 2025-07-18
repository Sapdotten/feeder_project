import subprocess
import time
import yaml
from configs import Config

process: subprocess.Popen


def setup():
    # чтение конфигурации
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    resolution = config['camera']['resolution']
    max_fps = config['camera']['max_fps']

    config = Config()
    rtsp_host = config.rtsp_host
    rtsp_port = config.rtsp_port
    rtsp_suffix = config.rtsp_suffix

    command = [
        'ffmpeg',
        '-f', 'v4l2',
        '-i', '/dev/video3',
        '-s', resolution,
        '-r', str(max_fps),
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-threads', '4',
        '-f', 'rtsp',
        f'rtsp://{rtsp_host}:{rtsp_port}/{rtsp_suffix}'
    ]
    # Запускаем команду
    global process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f'Запущен процесс ffmpeg с PID: {process.pid}')


def close():
    global process
    if process:
        process.terminate()  # Завершаем процесс корректно
        process.wait()  # Ждем завершения процесса
        print("Процесс ffmpeg завершен.")


if __name__ == "__main__":
    setup()
    time.sleep(60)
    close()
