# TRON Wallet Info Service

Микросервис для получения информации о TRON кошельках и хранения истории запросов.

## Функциональность

- Получение информации о bandwidth, energy и TRX балансе для TRON адреса
- Сохранение истории запросов в SQLite базу данных
- Получение истории запросов с пагинацией

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Wiquzix/torn
cd torn
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
# или
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Структура проекта
```
tztorn/
├── app/
│   ├── __init__.py
│   ├── main.py           # Основной файл приложения
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── database.py      # Конфигурация базы данных
│   └── services/        # Сервисы
├── tests/              # Тесты
└── requirements.txt    # Зависимости проекта
```

## Запуск

Для запуска сервиса выполните:
```bash
uvicorn app.main:app --reload
```

Сервис будет доступен по адресу http://localhost:8000

## API Endpoints

### POST /wallet
Получение информации о кошельке

Пример запроса:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/wallet?wallet_address=TWd4WrZ9wn84f5x1hZhL4DHvk738ns5jwb' \
  -H 'accept: application/json'
```

### GET /wallet/history
Получение истории запросов с пагинацией

Параметры запроса:
- skip (по умолчанию: 0)
- limit (по умолчанию: 10, максимум: 100)

## Тесты

Для запуска тестов выполните:
```bash
pytest
```
