# tests/api/test_habit_stats.py

from datetime import date, timedelta
from typing import Any
from uuid import uuid4

from fastapi.testclient import TestClient


def _create_habit(client: TestClient, *, type_: str = "numeric") -> str:
    body = {
        "name": "Test habit",
        "description": "Test description",
        "category": "Test",
        "type": type_,
        "goal": 10,
        "parent_id": None,
    }
    resp = client.post("/habits", json=body)
    assert resp.status_code == 200

    data: dict[str, Any] = resp.json()
    return str(data["id"])


def _add_log(client: TestClient, habit_id: str, d: date, value: float) -> None:
    body = {
        "date": d.isoformat(),
        "value": value,
    }
    resp = client.post(f"/habits/{habit_id}/logs", json=body)
    assert resp.status_code == 200


def test_stats_for_habit_without_logs_returns_zeroes(client: TestClient) -> None:
    habit_id = _create_habit(client)

    resp = client.get(f"/habits/{habit_id}/stats")
    assert resp.status_code == 200

    data = resp.json()
    assert data["habit_id"] == habit_id
    assert data["total"] == 0.0
    assert data["current_streak"] == 0
    assert data["average"] == 0.0


def test_stats_total_and_average_for_multiple_logs(client: TestClient) -> None:
    habit_id = _create_habit(client, type_="numeric")

    base = date(2025, 1, 1)
    _add_log(client, habit_id, base + timedelta(days=0), 1)  # 2025-01-01
    _add_log(client, habit_id, base + timedelta(days=1), 2)  # 2025-01-02
    _add_log(client, habit_id, base + timedelta(days=2), 3)  # 2025-01-03

    resp = client.get(f"/habits/{habit_id}/stats")
    assert resp.status_code == 200

    data = resp.json()
    assert data["habit_id"] == habit_id
    # total = 1 + 2 + 3 = 6
    assert data["total"] == 6.0
    # average = 6 / 3 = 2
    assert data["average"] == 2.0


def test_stats_current_streak_with_consecutive_days(client: TestClient) -> None:
    habit_id = _create_habit(client, type_="numeric")

    # three consecutive days
    base = date(2025, 1, 10)
    _add_log(client, habit_id, base + timedelta(days=0), 1)  # 10th
    _add_log(client, habit_id, base + timedelta(days=1), 1)  # 11th
    _add_log(client, habit_id, base + timedelta(days=2), 1)  # 12th

    resp = client.get(f"/habits/{habit_id}/stats")
    assert resp.status_code == 200

    data = resp.json()
    # last log is on 12th, previous on 11th and 10th → streak = 3
    assert data["current_streak"] == 3


def test_stats_current_streak_breaks_on_gap(client: TestClient) -> None:
    habit_id = _create_habit(client, type_="numeric")

    base = date(2025, 2, 1)
    # old log far in the past
    _add_log(client, habit_id, base + timedelta(days=0), 1)  # 1st
    # gap day (2nd) – no log
    # last logs on 3rd and 4th
    _add_log(client, habit_id, base + timedelta(days=2), 1)  # 3rd
    _add_log(client, habit_id, base + timedelta(days=3), 1)  # 4th

    resp = client.get(f"/habits/{habit_id}/stats")
    assert resp.status_code == 200

    data = resp.json()
    # Only 3rd and 4th are consecutive ending at last log date → streak = 2
    assert data["current_streak"] == 2


def test_stats_for_missing_habit_returns_404(client: TestClient) -> None:
    random_id = str(uuid4())

    resp = client.get(f"/habits/{random_id}/stats")
    assert resp.status_code == 404
