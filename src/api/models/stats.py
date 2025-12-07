# src/api/models/stats.py

from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class HabitStatsResponse(BaseModel):
    """
    Response model for habit statistics.
    """

    habit_id: UUID
    total: float
    current_streak: int
    average: float
