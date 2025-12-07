# src/api/routes/habit_logs_route.py

from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query

from src.api.models.habits import ErrorResponse
from src.api.models.logs import HabitLogCreate, HabitLogListResponse, HabitLogResponse
from src.core.services.habit_log_service import HabitLogService
from src.infra.repositories.habit_log_repository import SQLiteHabitLogRepository
from src.infra.repositories.habit_repository import SQLiteHabitRepository

# THIS must exist for app.py:
router = APIRouter(prefix="/habits", tags=["habit-logs"])

habit_repository = SQLiteHabitRepository()
habit_log_repository = SQLiteHabitLogRepository()
habit_log_service = HabitLogService(habit_log_repository, habit_repository)

# Ruff B008: use module-level singletons for Query defaults
START_DATE_QUERY = Query(
    None,
    description="Optional start date (inclusive).",
)
END_DATE_QUERY = Query(
    None,
    description="Optional end date (inclusive).",
)


@router.post(
    "/{habit_id}/logs",
    response_model=HabitLogResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
def add_log(habit_id: UUID, body: HabitLogCreate) -> HabitLogResponse:
    try:
        log = habit_log_service.add_log(
            habit_id=habit_id,
            log_date=body.date,
            value=body.value,
        )
    except ValueError as exc:
        msg = str(exc)
        if "not found" in msg:
            raise HTTPException(status_code=404, detail=msg) from exc
        raise HTTPException(status_code=400, detail=msg) from exc

    return HabitLogResponse(
        id=log.id,
        habit_id=log.habit_id,
        date=log.date,
        value=log.value,
    )


@router.get(
    "/{habit_id}/logs",
    response_model=HabitLogListResponse,
    responses={404: {"model": ErrorResponse}},
)
def list_logs(
    habit_id: UUID,
    start: date | None = START_DATE_QUERY,
    end: date | None = END_DATE_QUERY,
) -> HabitLogListResponse:
    try:
        logs = habit_log_service.list_logs(habit_id, start, end)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return HabitLogListResponse(
        logs=[
            HabitLogResponse(
                id=log.id,
                habit_id=log.habit_id,
                date=log.date,
                value=log.value,
            )
            for log in logs
        ]
    )
