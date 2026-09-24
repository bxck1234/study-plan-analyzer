import sqlite3
from datetime import datetime

from database.db import get_connection
from database.models import User
from utils.password import hash_password, verify_password


class AuthService:
    def register(self, username: str, nickname: str, password: str) -> tuple[bool, str]:
        try:
            password_hash, salt = hash_password(password)
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO users(username,nickname,password_hash,salt,created_at) VALUES(?,?,?,?,?)",
                    (username, nickname, password_hash, salt, datetime.now().isoformat(timespec="seconds")),
                )
            return True, "注册成功，请登录"
        except sqlite3.IntegrityError:
            return False, "用户名已存在"
        except sqlite3.Error:
            return False, "注册失败，请稍后重试"

    def login(self, username: str, password: str) -> User | None:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if not row or not verify_password(password, row["password_hash"], row["salt"]):
            return None
        return User(row["id"], row["username"], row["nickname"], row["created_at"])

    def update_nickname(self, user_id: int, nickname: str) -> bool:
        with get_connection() as conn:
            conn.execute("UPDATE users SET nickname=? WHERE id=?", (nickname, user_id))
        return True

    def update_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        with get_connection() as conn:
            row = conn.execute("SELECT password_hash,salt FROM users WHERE id=?", (user_id,)).fetchone()
            if not row or not verify_password(old_password, row["password_hash"], row["salt"]):
                return False, "当前密码不正确"
            password_hash, salt = hash_password(new_password)
            conn.execute("UPDATE users SET password_hash=?,salt=? WHERE id=?", (password_hash, salt, user_id))
        return True, "密码修改成功"

    def get_user(self, user_id: int) -> User | None:
        with get_connection() as conn:
            row = conn.execute("SELECT id,username,nickname,created_at FROM users WHERE id=?", (user_id,)).fetchone()
        return User(row["id"], row["username"], row["nickname"], row["created_at"]) if row else None

