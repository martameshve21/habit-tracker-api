# src/core/services/habit_service.py

from datetime import date
from uuid import UUID, uuid4

from src.core.entities.habit import Habit, HabitType
from src.core.interface.repositories import HabitRepository


class HabitService:
    """
    Application service for managing habits and sub-habits.
    """

    def __init__(self, habit_repository: HabitRepository) -> None:
        self._habit_repository = habit_repository

    def create_habit(
        self,
        name: str,
        description: str,
        category: str,
        type_: HabitType,
        goal: float | None,
        parent_id: UUID | None = None,
    ) -> Habit:
        habit = Habit(
            id=uuid4(),
            name=name,
            description=description,
            category=category,
            type=type_,
            goal=goal,
            created_at=date.today(),
            parent_id=parent_id,
        )
        self._habit_repository.create(habit)
        return habit

    def get_habit(self, habit_id: UUID) -> Habit:
        habit = self._habit_repository.get_by_id(habit_id)
        if habit is None:
            raise ValueError("Habit not found")
        return habit

    def list_habits(self) -> list[Habit]:
        return self._habit_repository.get_all()

    def update_habit(
        self,
        habit_id: UUID,
        name: str | None = None,
        description: str | None = None,
        category: str | None = None,
        goal: float | None = None,
        parent_id: UUID | None = None,
    ) -> Habit:
        habit = self.get_habit(habit_id)

        if name is not None:
            habit.name = name
        if description is not None:
            habit.description = description
        if category is not None:
            habit.category = category
        if goal is not None:
            habit.goal = goal
        if parent_id is not None:
            habit.parent_id = parent_id

        self._habit_repository.update(habit)
        return habit

    def delete_habit(self, habit_id: UUID) -> None:
        # ensure it exists first
        self.get_habit(habit_id)
        self._habit_repository.delete(habit_id)

    def create_subhabit(
        self,
        parent_id: UUID,
        name: str,
        description: str,
        category: str,
        type_: HabitType,
        goal: float | None,
    ) -> Habit:
        # ensure parent exists; will raise if not found
        self.get_habit(parent_id)

        return self.create_habit(
            name=name,
            description=description,
            category=category,
            type_=type_,
            goal=goal,
            parent_id=parent_id,
        )
