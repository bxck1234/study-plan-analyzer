from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    username: str
    nickname: str
    created_at: str


@dataclass
class Task:
    id: int
    user_id: int
    task_date: str
    subject: str
    task_name: str
    task_type: str
    planned_start_time: str
    planned_duration: int
    difficulty: str
    priority: str
    status: str
    notes: str = ""
    execution: Optional[dict] = None

