# src/api/models/logs.py

from __future__ import annotations

import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class HabitLogCreate(BaseModel):
    """
    Request body for creating a log for a habit.

    For boolean habits:
        - value = 1.0 means "done"
        - value = 0.0 means "not done"

    For numeric habits:
        - value is the measured quantity (minutes, pages, glasses, etc.).
    """

    date: dt.date = Field(
        default_factory=dt.date.today,
        description="Day this log belongs to.",
    )
    value: float = Field(
        ...,
        description="Progress value for the given date.",
        examples=[1.0],
    )


class HabitLogResponse(BaseModel):
    """
    Single log entry returned by the API.
    """

    id: UUID
    habit_id: UUID
    date: dt.date
    value: float


class HabitLogListResponse(BaseModel):
    """
    Response wrapper for listing multiple logs.
    """

    logs: list[HabitLogResponse]
