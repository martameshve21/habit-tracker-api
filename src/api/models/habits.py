# src/api/models/habits.py

from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field

from src.core.entities.habit import HabitType


class ErrorResponse(BaseModel):
    message: str


class HabitCreate(BaseModel):
    """
    Request body for creating a habit.
    """

    name: str = Field(
        ...,
        description="Name of the habit.",
        examples=["Drink 8 glasses of water"],
    )
    description: str = Field(
        ...,
        description="Short description of the habit.",
        examples=["Track daily water intake to stay hydrated."],
    )
    category: str = Field(
        ...,
        description="Category of the habit.",
        examples=["Health"],
    )
    type: HabitType = Field(
        ...,
        description="Habit type: boolean = done/not done, numeric = quantity.",
        examples=[HabitType.BOOLEAN],
    )
    goal: float | None = Field(
        default=None,
        description="Optional target value (e.g., 8 glasses, 20 pages).",
        examples=[8.0],
    )
    parent_id: UUID | None = Field(
        default=None,
        description="If set, this habit is a sub-habit of the given habit.",
    )


class HabitUpdate(BaseModel):
    """
    Request body for updating a habit.
    All fields are optional.
    """

    name: str | None = Field(None)
    description: str | None = Field(None)
    category: str | None = Field(None)
    goal: float | None = Field(None)
    parent_id: UUID | None = Field(None)


class HabitResponse(BaseModel):
    """
    Single habit representation in responses.
    """

    id: UUID
    name: str
    description: str
    category: str
    type: HabitType
    goal: float | None
    created_at: date
    parent_id: UUID | None


class HabitListResponse(BaseModel):
    """
    Response for listing habits.
    """

    habits: list[HabitResponse]
