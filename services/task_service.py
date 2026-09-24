import csv
from datetime import datetime
from pathlib import Path

from database.db import get_connection


class TaskService:
    def list_tasks(self, user_id: int, search: str = "", task_date: str = "", subject: str = "", status: str = "") -> list[dict]:
        sql = "SELECT * FROM tasks WHERE user_id=?"
        params: list = [user_id]
        if search:
            sql += " AND (task_name LIKE ? OR subject LIKE ?)"
            params += [f"%{search}%", f"%{search}%"]
        if task_date:
            sql += " AND task_date=?"; params.append(task_date)
        if subject and subject != "全部科目":
            sql += " AND subject=?"; params.append(subject)
        if status and status != "全部状态":
            sql += " AND status=?"; params.append(status)
        sql += " ORDER BY task_date DESC, planned_start_time ASC, id DESC"
        with get_connection() as conn:
            return [dict(r) for r in conn.execute(sql, params).fetchall()]

    def get_task(self, user_id: int, task_id: int) -> dict | None:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id=? AND user_id=?", (task_id, user_id)).fetchone()
        return dict(row) if row else None

    def save_task(self, user_id: int, data: dict, task_id: int | None = None) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        values = (data["task_date"], data["subject"], data["task_name"], data["task_type"], data["planned_start_time"], data["planned_duration"], data["difficulty"], data["priority"], data.get("status", "待完成"), data.get("notes", ""))
        with get_connection() as conn:
            if task_id:
                conn.execute("""UPDATE tasks SET task_date=?,subject=?,task_name=?,task_type=?,planned_start_time=?,planned_duration=?,difficulty=?,priority=?,status=?,notes=?,updated_at=? WHERE id=? AND user_id=?""", values + (now, task_id, user_id))
                return task_id
            cur = conn.execute("""INSERT INTO tasks(user_id,task_date,subject,task_name,task_type,planned_start_time,planned_duration,difficulty,priority,status,notes,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", (user_id,) + values + (now, now))
            return int(cur.lastrowid)

    def delete_task(self, user_id: int, task_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id=? AND user_id=?", (task_id, user_id))
        return cur.rowcount > 0

    def save_execution(self, user_id: int, task_id: int, data: dict) -> bool:
        now = datetime.now().isoformat(timespec="seconds")
        with get_connection() as conn:
            owned = conn.execute("SELECT id FROM tasks WHERE id=? AND user_id=?", (task_id, user_id)).fetchone()
            if not owned:
                return False
            conn.execute("""INSERT INTO execution_records(user_id,task_id,actual_start_time,actual_end_time,actual_duration,completion_level,completed,interrupted,self_evaluation,notes,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(task_id) DO UPDATE SET actual_start_time=excluded.actual_start_time,actual_end_time=excluded.actual_end_time,actual_duration=excluded.actual_duration,completion_level=excluded.completion_level,completed=excluded.completed,interrupted=excluded.interrupted,self_evaluation=excluded.self_evaluation,notes=excluded.notes""", (user_id, task_id, data.get("actual_start_time"), data.get("actual_end_time"), data["actual_duration"], data["completion_level"], int(data["completed"]), int(data["interrupted"]), data.get("self_evaluation", 3), data.get("notes", ""), now))
            status = "已完成" if data["completed"] else ("进行中" if data["actual_duration"] else "待完成")
            conn.execute("UPDATE tasks SET status=?,updated_at=? WHERE id=? AND user_id=?", (status, now, task_id, user_id))
        return True

    def clear_user_data(self, user_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE user_id=?", (user_id,))

    def export_csv(self, user_id: int, path: str) -> int:
        rows = self.list_tasks(user_id)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f); writer.writerow(["日期", "科目", "任务", "类型", "计划开始", "计划分钟", "状态"])
            writer.writerows([[r["task_date"], r["subject"], r["task_name"], r["task_type"], r["planned_start_time"], r["planned_duration"], r["status"]] for r in rows])
        return len(rows)

