# tests/api/test_habits.py
from typing import Any
from uuid import uuid4

from fastapi.testclient import TestClient


def _sample_habit_json() -> dict[str, Any]:
    return {
        "name": "Drink water",
        "description": "Drink 8 glasses of water",
        "category": "Health",
        "type": "boolean",
        "goal": 1,
        "parent_id": None,
    }


def test_create_habit_and_get_by_id(client: TestClient) -> None:
    # create
    create_resp = client.post("/habits", json=_sample_habit_json())
    assert create_resp.status_code == 200

    created = create_resp.json()
    habit_id = created["id"]

    # basic fields
    assert created["name"] == "Drink water"
    assert created["category"] == "Health"
    assert created["type"] == "boolean"
    assert created["goal"] == 1
    assert created["parent_id"] is None
    assert "created_at" in created

    # get by id
    get_resp = client.get(f"/habits/{habit_id}")
    assert get_resp.status_code == 200

    loaded = get_resp.json()
    assert loaded["id"] == habit_id
    assert loaded["name"] == created["name"]
    assert loaded["description"] == created["description"]
    assert loaded["category"] == created["category"]


def test_get_habit_not_found(client: TestClient) -> None:
    random_id = str(uuid4())

    resp = client.get(f"/habits/{random_id}")

    assert resp.status_code == 404
    body = resp.json()
    # from our route: HTTPException(status_code=404, detail="Habit not found")
    assert body["detail"] == "Habit not found"
