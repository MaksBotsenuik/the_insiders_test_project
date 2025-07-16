# Location Reviews API

**Location Reviews API** — це Django REST Framework застосунок для керування локаціями, категоріями та відгуками користувачів із системою лайків/дизлайків. Підтримує кешування через Redis та зберігання даних у Postgres.

## Можливості
- CRUD для локацій, категорій, адрес та відгуків
- Одна оцінка від користувача на локацію
- Лайки/дизлайки для відгуків
- Фільтрація та пошук локацій
- Пагінація
- Аутентифікація користувачів
- Кешування списку локацій та експорту через Redis

## Швидкий старт

1. **Клонувати репозиторій:**
   ```sh
   git clone <your-repo-url>
   cd inseders_test_task
   ```
2. **Встановити залежності:**
   ```sh
   pip install -r requirments.txt
   ```
3. **Запустити Redis через Docker Compose:**
   ```sh
   docker compose up -d
   ```
   > Це підніме лише Redis (порт 6379).
4. **Запустити Postgres (локально або через власний контейнер).**
   > Приклад для локального запуску Postgres:
   > - Створіть БД, користувача та пароль відповідно до налаштувань у settings.py або змінних середовища.
5. **Застосувати міграції:**
   ```sh
   python manage.py migrate
   ```
6. **Створити суперкористувача:**
   ```sh
   python manage.py createsuperuser
   ```
7. **Запустити сервер Django:**
   ```sh
   python manage.py runserver
   ```

---

## API

- **Swagger:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Redoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

### Основні ендпоінти
- `GET /api/v1/location/` — список локацій (кешується)
- `POST /api/v1/location/` — створити локацію
- `GET /api/v1/category/` — список категорій
- `GET /api/v1/review/` — список відгуків
- `POST /api/v1/review/` — залишити відгук
- `POST /api/v1/review/<id>/like/` — лайк
- `POST /api/v1/review/<id>/dislike/` — дизлайк
- `GET /api/v1/location/export/?type=csv` — експорт локацій у CSV (кешується)

### Аутентифікація
- Реєстрація: `/accounts/register/`
- Вхід: `/accounts/login/`
- Профіль: `/accounts/profile/`

### Приклад створення відгуку
```json
POST /api/v1/review/
{
  "rating": 5,
  "comment": "Чудове місце!",
  "location": 1
}
```

## Вимоги
- python: 3.10+
- postgresql: 17
- 
- Docker, Docker Compose

## Налаштування змінних середовища
- `DJANGO_DB_HOST`, `DJANGO_DB_PORT`, `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD` — для Postgres

---


