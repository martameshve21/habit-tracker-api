# src/core/entities/habit_stats.py

from dataclasses import dataclass
from uuid import UUID


@dataclass
class HabitStats:
    """
    Aggregate statistics for a single habit.
    - total: sum of all logged values
    - current_streak: consecutive days with logs, counting back from latest log
    - average: total / number_of_logs
    """

    habit_id: UUID
    total: float
    current_streak: int
    average: float
