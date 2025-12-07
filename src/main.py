# src/main.py

import uvicorn

from src.app import app
from src.infra.database import init_db


def main() -> None:
    init_db()  # <-- important
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
