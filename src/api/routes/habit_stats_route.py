# src/api/routes/habit_stats_route.py

from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.models.habits import ErrorResponse
from src.api.models.stats import HabitStatsResponse
from src.core.services.habit_stats_service import HabitStatsService
from src.infra.repositories.habit_repository import SQLiteHabitRepository
from src.infra.repositories.habit_stats_repository import SQLiteHabitStatsRepository

# THIS is what app.py imports
router = APIRouter(prefix="/habits", tags=["habit-stats"])

habit_repository = SQLiteHabitRepository()
habit_stats_repository = SQLiteHabitStatsRepository()
habit_stats_service = HabitStatsService(habit_stats_repository, habit_repository)


@router.get(
    "/{habit_id}/stats",
    response_model=HabitStatsResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_stats(habit_id: UUID) -> HabitStatsResponse:
    try:
        stats = habit_stats_service.get_stats(habit_id)
    except ValueError as exc:
        # B904: chain the original exception
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return HabitStatsResponse(
        habit_id=stats.habit_id,
        total=stats.total,
        current_streak=stats.current_streak,
        average=stats.average,
    )
