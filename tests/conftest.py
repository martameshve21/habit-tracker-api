# tests/conftest.py

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.infra.database import DB_PATH, init_db


@pytest.fixture(autouse=True)
def reset_db() -> Generator[None]:
    """
    For every test:
    - delete existing DB file (if any)
    - re-create schema
    - run the test
    - delete DB file again

    This keeps tests isolated from each other.
    """
    # make sure old DB is gone
    if isinstance(DB_PATH, Path):
        if DB_PATH.exists():
            DB_PATH.unlink()
    else:
        # fallback, if DB_PATH happened to be a string
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    # create tables
    init_db()

    yield

    # cleanup after test
    if isinstance(DB_PATH, Path):
        if DB_PATH.exists():
            DB_PATH.unlink()
    else:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
