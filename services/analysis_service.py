from collections import defaultdict
from datetime import date, timedelta

from database.db import get_connection
from utils.date_utils import date_range


def _records(user_id: int, where: str = "", params: tuple = ()) -> list[dict]:
    sql = """SELECT t.*, e.actual_start_time,e.actual_end_time,e.actual_duration,e.completion_level,e.completed,e.interrupted,e.self_evaluation FROM tasks t LEFT JOIN execution_records e ON e.task_id=t.id AND e.user_id=t.user_id WHERE t.user_id=?"""
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql + (" AND " + where if where else "") + " ORDER BY t.task_date", (user_id,) + params).fetchall()]


def get_plan_execution_deviation(planned: int, actual: int | None) -> tuple[int, float]:
    if actual is None: return 0, 0.0
    delta = actual - planned
    return delta, (delta / planned * 100) if planned else 0.0


def get_daily_summary(user_id: int, day: str | None = None) -> dict:
    day = day or date.today().isoformat(); rows = _records(user_id, "t.task_date=?", (day,))
    valid = [r for r in rows if r["actual_duration"] is not None]
    deviations = [get_plan_execution_deviation(r["planned_duration"], r["actual_duration"])[1] for r in valid]
    return {"date": day, "planned_count": len(rows), "completed_count": sum(bool(r["completed"]) for r in rows), "completion_rate": (sum(bool(r["completed"]) for r in rows) / len(rows) * 100 if rows else 0), "avg_deviation": (sum(deviations) / len(deviations) if deviations else 0), "tasks": rows}


def get_weekly_summary(user_id: int) -> dict:
    days = date_range(7); rows = _records(user_id, "t.task_date BETWEEN ? AND ?", (days[0], days[-1]))
    return {"planned_count": len(rows), "completed_count": sum(bool(r["completed"]) for r in rows), "completion_rate": (sum(bool(r["completed"]) for r in rows) / len(rows) * 100 if rows else 0), "days": days}


def _group_stats(rows: list[dict], key: str) -> list[dict]:
    groups = defaultdict(list)
    for r in rows: groups[r[key]].append(r)
    result = []
    for name, items in groups.items():
        valid = [r for r in items if r["actual_duration"] is not None]
        rates = [get_plan_execution_deviation(r["planned_duration"], r["actual_duration"])[1] for r in valid]
        result.append({"name": name, "count": len(items), "completed": sum(bool(r["completed"]) for r in items), "avg_planned": sum(r["planned_duration"] for r in items) / len(items), "avg_actual": sum(r["actual_duration"] for r in valid) / len(valid) if valid else 0, "avg_deviation": sum(get_plan_execution_deviation(r["planned_duration"], r["actual_duration"])[0] for r in valid) / len(valid) if valid else 0, "avg_rate": sum(rates) / len(rates) if rates else 0, "completion_rate": sum(bool(r["completed"]) for r in items) / len(items) * 100})
    return sorted(result, key=lambda x: x["count"], reverse=True)


def get_subject_statistics(user_id: int) -> list[dict]: return _group_stats(_records(user_id), "subject")
def get_task_type_statistics(user_id: int) -> list[dict]: return _group_stats(_records(user_id), "task_type")


def _period(start: str | None) -> str:
    if not start: return "未记录"
    hour = int(start[:2])
    if hour < 9: return "06:00–09:00"
    if hour < 12: return "09:00–12:00"
    if hour < 15: return "12:00–15:00"
    if hour < 18: return "15:00–18:00"
    if hour < 21: return "18:00–21:00"
    return "21:00–24:00"


def get_time_period_statistics(user_id: int) -> list[dict]:
    rows = _records(user_id); groups = defaultdict(list)
    for r in rows: groups[_period(r["actual_start_time"] or r["planned_start_time"])].append(r)
    return [{"name": k, "count": len(v), "completion_rate": sum(bool(r["completed"]) for r in v) / len(v) * 100, "avg_rate": sum(get_plan_execution_deviation(r["planned_duration"], r["actual_duration"])[1] for r in v if r["actual_duration"] is not None) / max(1, sum(r["actual_duration"] is not None for r in v)), "complete_rate": sum(r.get("completion_level") == "完全完成" for r in v) / len(v) * 100} for k, v in groups.items()]


def get_recent_trend(user_id: int, days: int = 30) -> list[dict]:
    result = []
    for d in date_range(days):
        rows = _records(user_id, "t.task_date=?", (d,)); valid = [r for r in rows if r["actual_duration"] is not None]
        result.append({"date": d, "planned": sum(r["planned_duration"] for r in rows), "actual": sum(r["actual_duration"] for r in valid), "completion_rate": sum(bool(r["completed"]) for r in rows) / len(rows) * 100 if rows else 0, "avg_rate": sum(get_plan_execution_deviation(r["planned_duration"], r["actual_duration"])[1] for r in valid) / len(valid) if valid else 0})
    return result

