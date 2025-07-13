Код для кошачьих кормушек.

Подключение к netbird:
```sh
sudo netbird up --setup-key <SETUP KEY>
```

Запуск бэка:
```sh
pip install -r requirements
uvicorn src.app:app --reload --port 8000 --host 0.0.0.0
```