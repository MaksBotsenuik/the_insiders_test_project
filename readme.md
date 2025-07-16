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
2. **Створити файл .env у корені проєкту:**
   ```env
   DB_NAME=review_service
   DB_USER=postgres
   DB_PASSWORD=qweasdzxc123
   DB_HOST=db
   DB_PORT=5432 

   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=admin123
   ```
3. **Запустити всі сервіси через Docker Compose:**
   ```sh
   docker-compose down -v
   docker-compose up --build
   ```
   > Це підніме Django, Postgres і Redis, застосує міграції та автоматично створить суперкористувача.
4. **Відкрити Swagger:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
5. **Увійти в адмінку:** [http://localhost:8000/admin/](http://localhost:8000/admin/) (логін/пароль з .env)

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
- Реєстрація: `/register/`
- Вхід: `/accounts//login/`
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
- Python 3.10+
- Docker, Docker Compose

## Налаштування змінних середовища
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — для Postgres
- `REDIS_URL` — для Redis
- `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` — для автоматичного створення суперкористувача

### Приклад .env
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

## Запуск через Docker Compose
1. Створіть файл `.env` у корені проєкту з вмістом, як вище.
2. Запустіть:
   ```sh
   docker-compose down -v
   docker-compose up --build
   ```
3. Після запуску автоматично створиться суперкористувач з вказаними у .env даними.

---


