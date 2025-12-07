# src/infra/repositories/habit_stats_repository.py

from datetime import date, timedelta
from uuid import UUID

from src.core.entities.habit_stats import HabitStats
from src.core.interface.repositories import HabitStatsRepository
from src.infra.database import get_db


class SQLiteHabitStatsRepository(HabitStatsRepository):
    """
    SQLite implementation of HabitStatsRepository.

    Statistics per habit:
    - total:   sum of all logged values for this habit
    - average: total / number_of_logs
    - current_streak:
        number of consecutive days with at least one log,
        counting backwards from the most recent log date.
    """

    def get_stats(self, habit_id: UUID) -> HabitStats:
        # Fetch all logs for this habit, ordered by date
        with get_db() as db:
            rows = db.execute(
                """
                SELECT date, value
                  FROM habit_logs
                 WHERE habit_id = ?
              ORDER BY date ASC
                """,
                (str(habit_id),),
            ).fetchall()

        # No logs → empty stats
        if not rows:
            return HabitStats(
                habit_id=habit_id,
                total=0.0,
                current_streak=0,
                average=0.0,
            )

        # Convert rows to Python types
        dates: list[date] = []
        values: list[float] = []

        for row in rows:
            dates.append(date.fromisoformat(row["date"]))
            values.append(float(row["value"]))

        total = sum(values)
        count = len(values)
        average = total / count if count > 0 else 0.0

        # --- current streak calculation ---
        # Start from the last (most recent) log date
        last_date = dates[-1]
        streak = 1
        expected = last_date - timedelta(days=1)

        # Walk backward through previous dates
        for idx in range(len(dates) - 2, -1, -1):
            current_date = dates[idx]

            if current_date == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif current_date < expected:
                break
            else:
                break

        return HabitStats(
            habit_id=habit_id,
            total=total,
            current_streak=streak,
            average=average,
        )
