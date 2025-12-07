# src/core/services/habit_log_service.py

from datetime import date
from uuid import UUID, uuid4

from src.core.entities.habit import HabitType
from src.core.entities.habit_log import HabitLog
from src.core.interface.repositories import HabitLogRepository, HabitRepository


class HabitLogService:
    """
    Application service for managing habit logs.
    """

    def __init__(
        self,
        log_repository: HabitLogRepository,
        habit_repository: HabitRepository,
    ) -> None:
        self._log_repository = log_repository
        self._habit_repository = habit_repository

    def add_log(
        self,
        habit_id: UUID,
        log_date: date,
        value: float,
    ) -> HabitLog:
        # ensure habit exists
        habit = self._habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")

        # type-specific validation
        if habit.type == HabitType.BOOLEAN and value not in (0.0, 1.0):
            raise ValueError("Boolean habits must have value 0 or 1")

        log = HabitLog(
            id=uuid4(),
            habit_id=habit_id,
            date=log_date,
            value=value,
        )
        self._log_repository.create(log)
        return log

    def list_logs(
        self,
        habit_id: UUID,
        start: date | None = None,
        end: date | None = None,
    ) -> list[HabitLog]:
        # ensure habit exists
        habit = self._habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")

        return self._log_repository.list_for_habit(habit_id, start, end)
