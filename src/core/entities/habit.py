# src/core/entities/habit.py

from dataclasses import dataclass
from datetime import date
from enum import Enum
from uuid import UUID


class HabitType(str, Enum):
    """
    Type of habit:
    - boolean: done / not done (store 0 or 1 in logs)
    - numeric: quantity (pages, minutes, glasses, etc.)
    """
    BOOLEAN = "boolean"
    NUMERIC = "numeric"


@dataclass
class Habit:
    """
    Domain entity representing a habit.
    """

    id: UUID
    name: str
    description: str
    category: str
    type: HabitType
    goal: float | None
    created_at: date
    parent_id: UUID | None  # for sub-habits / routines
