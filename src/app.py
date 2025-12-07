# src/app.py

from fastapi import FastAPI

from src.api.routes.habit_logs_route import router as habit_logs_router
from src.api.routes.habit_stats_route import router as habit_stats_router
from src.api.routes.habits_route import router as habits_router
from src.infra.database import init_db

app = FastAPI(
    title="Smart Habit Tracker API",
    version="1.0.0",
)


@app.on_event("startup")
def startup() -> None:
    """Create tables if they don't exist (habits, habit_logs)."""
    init_db()


app.include_router(habits_router)
app.include_router(habit_logs_router)
app.include_router(habit_stats_router)
