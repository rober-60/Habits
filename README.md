# Habit Tracker — Backend

REST API do śledzenia nawyków — użytkownik rejestruje się, dodaje nawyki, oznacza ich wykonanie każdego dnia i widzi statystyki (streak, procent wykonania). Napisane w FastAPI, z pełnym auth, testami i konteneryzacją.

Frontend (React) w osobnym repo: [habit-tracker-frontend](https://github.com/TWOJA_NAZWA/habit-tracker-frontend).

## Funkcje

- Rejestracja i logowanie z JWT (hasła hashowane przez bcrypt)
- CRUD na nawykach (dodawanie, lista, edycja, usuwanie) — każdy user widzi tylko swoje
- Oznaczanie nawyku jako wykonanego danego dnia
- Streak liczony osobno dla nawyków dziennych i tygodniowych
- Procent wykonania w ostatnich 7 dniach
- Historia wykonań (do heatmapy w stylu GitHub contribution graph)
- Automatyczna dokumentacja API (Swagger UI pod `/docs`)

## Stack

- **FastAPI** — framework, automatyczna walidacja przez Pydantic, dokumentacja out-of-the-box
- **PostgreSQL** — baza danych
- **SQLAlchemy 2.0** — ORM
- **Alembic** — migracje bazy danych
- **JWT (python-jose)** — autoryzacja
- **pytest + httpx** — testy, na osobnej bazie testowej
- **Docker + docker-compose** — konteneryzacja

## Model danych

```
User
├── id, email, hashed_password, created_at

Habit
├── id, user_id (FK), name, frequency (daily/weekly), notes, created_at

HabitLog
├── id, habit_id (FK), date, completed
```

## Uruchomienie lokalnie (Docker)

```bash
git clone https://github.com/TWOJA_NAZWA/habit-tracker.git
cd habit-tracker
docker-compose up --build
```

API wystartuje pod `http://localhost:8000`, dokumentacja pod `http://localhost:8000/docs`.

Migracje bazy odpalają się automatycznie przy starcie kontenera.

## Uruchomienie lokalnie (bez Dockera)

Wymaga lokalnego Postgresa.

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload
```

## Testy

```bash
pytest tests/ -v
```

Testy działają na osobnej bazie testowej (`habits_test`), niezależnej od bazy developerskiej — każdy test startuje z czystymi tabelami. W CI (GitHub Actions) baza testowa jest odpalana jako serwis w workflow.

## Struktura projektu

```
app/
├── main.py           # inicjalizacja FastAPI, CORS, routery
├── models.py          # modele SQLAlchemy
├── schemas.py          # modele Pydantic
├── database.py         # połączenie z bazą
├── auth.py            # hashowanie haseł, JWT, get_current_user
└── routers/
    ├── auth.py          # /auth/register, /auth/login
    ├── habits.py         # CRUD na nawykach
    └── logs.py           # oznaczanie wykonania, statystyki, historia
alembic/              # migracje
tests/                # testy pytest
```
