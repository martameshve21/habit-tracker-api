# src/infra/repositories/habit_log_repository.py

from datetime import date
from uuid import UUID

from src.core.entities.habit_log import HabitLog
from src.core.interface.repositories import HabitLogRepository
from src.infra.database import get_db


class SQLiteHabitLogRepository(HabitLogRepository):
    """SQLite implementation of HabitLogRepository."""

    def create(self, log: HabitLog) -> None:
        with get_db() as db:
            db.execute(
                """
                INSERT INTO habit_logs (
                    id,
                    habit_id,
                    date,
                    value
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(log.id),
                    str(log.habit_id),
                    log.date.isoformat(),
                    log.value,
                ),
            )
            db.commit()

    def list_for_habit(
        self,
        habit_id: UUID,
        start: date | None = None,
        end: date | None = None,
    ) -> list[HabitLog]:
        query = """
            SELECT
                id,
                habit_id,
                date,
                value
            FROM habit_logs
            WHERE habit_id = ?
        """
        params: list[str] = [str(habit_id)]

        if start is not None:
            query += " AND date >= ?"
            params.append(start.isoformat())
        if end is not None:
            query += " AND date <= ?"
            params.append(end.isoformat())

        query += " ORDER BY date ASC"

        with get_db() as db:
            rows = db.execute(query, params).fetchall()

        logs: list[HabitLog] = []
        for row in rows:
            logs.append(
                HabitLog(
                    id=UUID(row["id"]),
                    habit_id=UUID(row["habit_id"]),
                    date=date.fromisoformat(row["date"]),
                    value=row["value"],
                )
            )
        return logs
