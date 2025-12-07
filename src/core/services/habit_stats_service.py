# src/core/services/habit_stats_service.py

from uuid import UUID

from src.core.entities.habit_stats import HabitStats
from src.core.interface.repositories import HabitRepository, HabitStatsRepository


class HabitStatsService:
    """
    Application service for fetching statistics for a habit.
    """

    def __init__(
        self,
        stats_repository: HabitStatsRepository,
        habit_repository: HabitRepository,
    ) -> None:
        self._stats_repository = stats_repository
        self._habit_repository = habit_repository

    def get_stats(self, habit_id: UUID) -> HabitStats:
        # ensure habit exists
        habit = self._habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")

        return self._stats_repository.get_stats(habit_id)
