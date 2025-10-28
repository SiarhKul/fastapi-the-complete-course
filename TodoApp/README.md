# FastAPI: The Complete Course
https://github.com/SiarhKul/fastapi-the-complete-course/tree/Project3
This is the repository for the learning project "FastAPI: The Complete Course".

## 🚀 Getting Started

This project uses **Poetry** for dependency management and virtual environments.

### Prerequisites

Before you begin, make sure you have installed:

* **Python** (version 3.11 or higher)
* **Poetry** ([installation guide](https://python-poetry.org/docs/#installation))

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your repository URL>
    cd fastapi-the-complete-course
    ```

2.  **Install dependencies:**
    Run `poetry install`. It will automatically create a virtual environment in the project directory and install all required packages from `pyproject.toml`.
    ```bash
    pip install -r requirements.txt
    python -m pip install --upgrade pip
    pip freeze > requirements.txt
    ```

## 🏃 Running the Application

1.  **Activate the virtual environment:**
    To ensure all commands run in the correct environment, activate it:
    ```bash
    poetry shell
    ```

2.  **Start the development server:**
    Use `uvicorn` to run your FastAPI application.
    ```bash
    source fastapienv/Scripts/activate
    uvicorn main:app --reload --port 8090
    ```
    * `main`: the `main.py` file.
    * `app`: the `app = FastAPI()` instance created in `main.py`.
    * `--reload`: automatically restarts the server when code changes are detected.

3.  **Open the API documentation:**
    After the server starts, open one of the following URLs in your browser:
    * **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## ✅ Testing and Formatting

* **Run tests:**
    To run the tests, use `pytest`:
    ```bash
    pytest
    ```

* **Code formatting:**
    The project uses `black` for automatic code formatting. To format all files, run:
    ```bash
    black .
    ```

## 🗄️ Database migrations (Alembic)

This project uses Alembic for schema migrations. Alembic is already configured to use the local SQLite database file `todosapp.db` (see `alembic.ini`) and `alembic/env.py` is set to use the project's SQLAlchemy metadata (`models.Base.metadata`) for autogeneration.

Below are common commands you'll use when creating and applying migrations. Pick the set that matches how you manage your environment (Poetry or a normal venv / pip).

Notes:
- If autogenerate doesn't detect changes, make sure your models are imported and `target_metadata = models.Base.metadata` is set in `alembic/env.py` (this project already does this).
- If you want Alembic to target a different database, edit the `sqlalchemy.url` value in `alembic.ini`.


1. Create an autogenerate migration (will compare models -> metadata -> DB):

```bash
poetry run alembic revision --autogenerate -m "describe change here"
```

2. Apply migrations to the database:

```bash
poetry run alembic upgrade head
```

Using a normal venv / pip-installed environment (Windows)

1. Create / activate your venv (example):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install requirements if not already installed:

```powershell
pip install -r requirements.txt
```

3. Create a migration with autogenerate:

```powershell
alembic revision --autogenerate -m "describe change here"
```

4. Apply migrations:

```powershell
alembic upgrade head
```

Useful Alembic commands

- Show current revision applied to DB:

```bash
alembic current
```

- Show migration history:

```bash
alembic history --verbose
```

- Create an empty/manual migration (no autogenerate):

```bash
alembic revision -m "manual migration" --empty
```

- Roll back one revision:

```bash
alembic downgrade -1
```

Troubleshooting

- If an autogenerate revision is empty but you expect changes: verify that the new/modified model is imported by `alembic/env.py` (the file already imports `models`) and that model classes are attached to `models.Base`.
- If you need to target a different database for running migrations, update `sqlalchemy.url` in `alembic.ini` (for temporary overrides you can also set environment variables or modify `env.py` to read the DB URL from an env var).

That's it — once you create revisions and run `alembic upgrade head`, your `todosapp.db` will be updated to match the SQLAlchemy models.
