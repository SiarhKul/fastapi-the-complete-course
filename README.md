# FastAPI: The Complete Course

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
    poetry install
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
    uvicorn main:app --reload
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