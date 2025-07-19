Код для кошачьих кормушек.

Подключение к netbird:
```sh
sudo netbird up --setup-key <SETUP KEY>
```

Запуск бэка:
```sh
pip install -r requirements
uvicorn src.app:app --reload --port 8000 --host 0.0.0.0
// sudo $(which uvicorn) src.app:app --reload --host 0.0.0.0 --port 8000
```

Установка mediamtx: 
```sh
wget https://github.com/bluenviron/mediamtx/releases/download/v1.13.0/mediamtx_v1.13.0_linux_arm64.tar.gz
tar -xvzf mediamtx_v1.13.0_linux_arm64.tar.gz
```

Проверка видеопотока:
```sh
vlc rtsp://192.168.68.110:8554/stream --rtsp-tcp
```