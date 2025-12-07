# src/api/routes/habits_route.py

from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.models.habits import (
    ErrorResponse,
    HabitCreate,
    HabitListResponse,
    HabitResponse,
    HabitUpdate,
)
from src.core.services.habit_service import HabitService
from src.infra.repositories.habit_repository import SQLiteHabitRepository

# THIS is what app.py imports
router = APIRouter(prefix="/habits", tags=["habits"])

habit_repository = SQLiteHabitRepository()
habit_service = HabitService(habit_repository)


@router.post(
    "",
    response_model=HabitResponse,
    responses={400: {"model": ErrorResponse}},
)
def create_habit(body: HabitCreate) -> HabitResponse:
    try:
        habit = habit_service.create_habit(
            name=body.name,
            description=body.description,
            category=body.category,
            type_=body.type,
            goal=body.goal,
            parent_id=body.parent_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        category=habit.category,
        type=habit.type,
        goal=habit.goal,
        created_at=habit.created_at,
        parent_id=habit.parent_id,
    )


@router.get(
    "",
    response_model=HabitListResponse,
)
def list_habits() -> HabitListResponse:
    habits = habit_service.list_habits()
    return HabitListResponse(
        habits=[
            HabitResponse(
                id=h.id,
                name=h.name,
                description=h.description,
                category=h.category,
                type=h.type,
                goal=h.goal,
                created_at=h.created_at,
                parent_id=h.parent_id,
            )
            for h in habits
        ]
    )


@router.get(
    "/{habit_id}",
    response_model=HabitResponse,
    responses={404: {"model": ErrorResponse}},
)
def get_habit(habit_id: UUID) -> HabitResponse:
    try:
        habit = habit_service.get_habit(habit_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        category=habit.category,
        type=habit.type,
        goal=habit.goal,
        created_at=habit.created_at,
        parent_id=habit.parent_id,
    )


@router.put(
    "/{habit_id}",
    response_model=HabitResponse,
    responses={404: {"model": ErrorResponse}},
)
def update_habit(habit_id: UUID, body: HabitUpdate) -> HabitResponse:
    try:
        habit = habit_service.update_habit(
            habit_id=habit_id,
            name=body.name,
            description=body.description,
            category=body.category,
            goal=body.goal,
            parent_id=body.parent_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        category=habit.category,
        type=habit.type,
        goal=habit.goal,
        created_at=habit.created_at,
        parent_id=habit.parent_id,
    )


@router.delete(
    "/{habit_id}",
    status_code=200,
    responses={404: {"model": ErrorResponse}},
)
def delete_habit(habit_id: UUID) -> dict[str, str]:
    try:
        habit_service.delete_habit(habit_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {}


@router.post(
    "/{habit_id}/subhabits",
    response_model=HabitResponse,
    responses={404: {"model": ErrorResponse}, 400: {"model": ErrorResponse}},
)
def create_subhabit(habit_id: UUID, body: HabitCreate) -> HabitResponse:
    try:
        habit = habit_service.create_subhabit(
            parent_id=habit_id,
            name=body.name,
            description=body.description,
            category=body.category,
            type_=body.type,
            goal=body.goal,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return HabitResponse(
        id=habit.id,
        name=habit.name,
        description=habit.description,
        category=habit.category,
        type=habit.type,
        goal=habit.goal,
        created_at=habit.created_at,
        parent_id=habit.parent_id,
    )
