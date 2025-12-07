# src/infra/repositories/habit_repository.py

from datetime import date
from uuid import UUID

from src.core.entities.habit import Habit, HabitType
from src.core.interface.repositories import HabitRepository
from src.infra.database import get_db


class SQLiteHabitRepository(HabitRepository):
    """SQLite implementation of HabitRepository."""

    def create(self, habit: Habit) -> None:
        with get_db() as db:
            db.execute(
                """
                INSERT INTO habits (
                    id,
                    name,
                    description,
                    category,
                    type,
                    goal,
                    created_at,
                    parent_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(habit.id),
                    habit.name,
                    habit.description,
                    habit.category,
                    habit.type.value,
                    habit.goal,
                    habit.created_at.isoformat(),
                    str(habit.parent_id) if habit.parent_id else None,
                ),
            )
            db.commit()

    def get_by_id(self, habit_id: UUID) -> Habit | None:
        with get_db() as db:
            row = db.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    category,
                    type,
                    goal,
                    created_at,
                    parent_id
                FROM habits
                WHERE id = ?
                """,
                (str(habit_id),),
            ).fetchone()

        if row is None:
            return None

        return Habit(
            id=UUID(row["id"]),
            name=row["name"],
            description=row["description"],
            category=row["category"],
            type=HabitType(row["type"]),
            goal=row["goal"],
            created_at=date.fromisoformat(row["created_at"]),
            parent_id=UUID(row["parent_id"]) if row["parent_id"] else None,
        )

    def get_all(self) -> list[Habit]:
        with get_db() as db:
            rows = db.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    category,
                    type,
                    goal,
                    created_at,
                    parent_id
                FROM habits
                ORDER BY created_at ASC, name ASC
                """
            ).fetchall()

        habits: list[Habit] = []
        for row in rows:
            habits.append(
                Habit(
                    id=UUID(row["id"]),
                    name=row["name"],
                    description=row["description"],
                    category=row["category"],
                    type=HabitType(row["type"]),
                    goal=row["goal"],
                    created_at=date.fromisoformat(row["created_at"]),
                    parent_id=UUID(row["parent_id"]) if row["parent_id"] else None,
                )
            )
        return habits

    def update(self, habit: Habit) -> None:
        with get_db() as db:
            db.execute(
                """
                UPDATE habits
                SET
                    name = ?,
                    description = ?,
                    category = ?,
                    type = ?,
                    goal = ?,
                    created_at = ?,
                    parent_id = ?
                WHERE id = ?
                """,
                (
                    habit.name,
                    habit.description,
                    habit.category,
                    habit.type.value,
                    habit.goal,
                    habit.created_at.isoformat(),
                    str(habit.parent_id) if habit.parent_id else None,
                    str(habit.id),
                ),
            )
            db.commit()

    def delete(self, habit_id: UUID) -> None:
        with get_db() as db:
            # delete logs first to keep referential integrity
            db.execute(
                "DELETE FROM habit_logs WHERE habit_id = ?",
                (str(habit_id),),
            )
            db.execute(
                "DELETE FROM habits WHERE id = ?",
                (str(habit_id),),
            )
            db.commit()
