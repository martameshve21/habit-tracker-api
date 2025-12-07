# tests/api/test_habit_logs.py

from datetime import date
from typing import Any
from uuid import uuid4

from fastapi.testclient import TestClient


def _create_habit(client: TestClient) -> str:
    habit_json = {
        "name": "Read book",
        "description": "Read 10 pages",
        "category": "Learning",
        "type": "numeric",
        "goal": 10,
        "parent_id": None,
    }
    resp = client.post("/habits", json=habit_json)
    assert resp.status_code == 200

    body: dict[str, Any] = resp.json()
    return str(body["id"])


def test_create_log_for_existing_habit(client: TestClient) -> None:
    habit_id = _create_habit(client)

    log_json = {
        "date": date.today().isoformat(),
        "value": 5,
    }

    resp = client.post(f"/habits/{habit_id}/logs", json=log_json)
    assert resp.status_code == 200

    body = resp.json()
    assert body["habit_id"] == habit_id
    assert body["date"] == log_json["date"]
    assert body["value"] == log_json["value"]


def test_create_log_for_missing_habit_returns_404(client: TestClient) -> None:
    random_id = str(uuid4())

    log_json = {
        "date": date.today().isoformat(),
        "value": 1,
    }

    resp = client.post(f"/habits/{random_id}/logs", json=log_json)

    # from our service: we raise ValueError("Habit not found") → route maps to 404
    assert resp.status_code == 404
