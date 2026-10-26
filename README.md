# Notes API

Это мой проект — простой REST API для заметок, который я написал в процессе изучения Python и фреймворка FastAPI.

Пока что это учебная версия. Данные хранятся не в базе данных, а просто в списке в оперативной памяти (in-memory). То есть при перезапуске сервера все заметки исчезают.

## Что использовал (Стек)
*   **Python** 
*   **FastAPI** — сам фреймворк для API
*   **Pydantic** — для валидации данных (проверяет, что заголовок не пустой и не слишком длинный)
*   **Uvicorn** — сервер, на котором всё это крутится

## Как запустить у себя

1. Скачиваем проект:
   ```bash
   git clone https://github.com/ваш_ник/notes-api.git
   cd notes-api
   
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

После запуска сервера интерактивная документация (Swagger UI) доступна по адресу:   http://127.0.0.1:8000/docs

Список эндпоинтов:
GET /health — проверка статуса сервера.

GET /hello — тестовый эндпоинт.

GET /notes — получить список всех заметок.

GET /notes/{id} — получить одну заметку по её ID.

POST /notes — создать новую заметку.

1. Создание заметки (POST /notes)
Request (JSON):

json
{
  "title": "Купить хлеб",
  "content": "Обязательно взять бородинский"
}
Response (201 Created):

json
{
  "title": "Купить хлеб",
  "content": "Обязательно взять бородинский",
  "id": 1
}
2. Получение списка заметок (GET /notes)
Response (200 OK):

json
[
  {
    "title": "Купить хлеб",
    "content": "Обязательно взять бородинский",
    "id": 1
  }
]