# src/core/entities/habit_log.py

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass
class HabitLog:
    """
    Single log entry for a habit on a specific date.
    """

    id: UUID
    habit_id: UUID
    date: date
    value: float  # 0/1 for boolean habits, numeric value for numeric habits
