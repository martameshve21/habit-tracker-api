# src/core/interface/repositories.py

from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from src.core.entities.habit import Habit
from src.core.entities.habit_log import HabitLog
from src.core.entities.habit_stats import HabitStats


class HabitRepository(ABC):
    """
    Abstraction for persisting and retrieving Habit entities.
    """

    @abstractmethod
    def create(self, habit: Habit) -> None:
        ...

    @abstractmethod
    def get_by_id(self, habit_id: UUID) -> Habit | None:
        ...

    @abstractmethod
    def get_all(self) -> list[Habit]:
        ...

    @abstractmethod
    def update(self, habit: Habit) -> None:
        ...

    @abstractmethod
    def delete(self, habit_id: UUID) -> None:
        ...


class HabitLogRepository(ABC):
    """
    Abstraction for persisting and retrieving HabitLog entries.
    """

    @abstractmethod
    def create(self, log: HabitLog) -> None:
        ...

    @abstractmethod
    def list_for_habit(
        self,
        habit_id: UUID,
        start: date | None = None,
        end: date | None = None,
    ) -> list[HabitLog]:
        ...


class HabitStatsRepository(ABC):
    """
    Abstraction for computing or retrieving statistics for a habit.
    """

    @abstractmethod
    def get_stats(self, habit_id: UUID) -> HabitStats:
        ...
