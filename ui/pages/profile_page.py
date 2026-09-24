from PySide6.QtWidgets import QFileDialog, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
from services.auth_service import AuthService
from services.task_service import TaskService


class ProfilePage(QWidget):
    def __init__(self, user, on_changed):
        super().__init__(); self.user = user; self.on_changed = on_changed; self.auth = AuthService(); self.tasks = TaskService(); layout = QVBoxLayout(self); title = QLabel("我的"); title.setObjectName("pageTitle"); layout.addWidget(title); self.info = QLabel(); layout.addWidget(self.info); form = QFormLayout(); self.nickname = QLineEdit(user.nickname); self.old = QLineEdit(); self.old.setEchoMode(QLineEdit.EchoMode.Password); self.new = QLineEdit(); self.new.setEchoMode(QLineEdit.EchoMode.Password); form.addRow("昵称", self.nickname); layout.addLayout(form); save = QPushButton("保存昵称"); save.clicked.connect(self.save_nickname); form2 = QFormLayout(); form2.addRow("当前密码", self.old); form2.addRow("新密码", self.new); layout.addLayout(form2); pwd = QPushButton("修改密码"); pwd.clicked.connect(self.save_password); export = QPushButton("导出我的数据 CSV"); export.clicked.connect(self.export); clear = QPushButton("清空我的学习记录"); clear.clicked.connect(self.clear); layout.addWidget(save); layout.addWidget(pwd); layout.addWidget(export); layout.addWidget(clear); layout.addStretch(); self.refresh()
    def refresh(self):
        rows = self.tasks.list_tasks(self.user.id); total = sum((r["planned_duration"] for r in rows), 0); self.info.setText(f"用户名：{self.user.username}\n注册时间：{self.user.created_at}\n累计学习任务：{len(rows)} 条\n计划学习时间：{total} 分钟")
    def save_nickname(self):
        if self.nickname.text().strip(): self.auth.update_nickname(self.user.id, self.nickname.text().strip()); self.user.nickname = self.nickname.text().strip(); self.on_changed(); QMessageBox.information(self, "提示", "昵称已更新")
    def save_password(self):
        if len(self.new.text()) < 6: QMessageBox.warning(self, "提示", "新密码至少6位"); return
        ok, msg = self.auth.update_password(self.user.id, self.old.text(), self.new.text()); QMessageBox.information(self, "提示", msg) if ok else QMessageBox.warning(self, "提示", msg)
    def export(self):
        path, _ = QFileDialog.getSaveFileName(self, "导出数据", "study_data.csv", "CSV 文件 (*.csv)")
        if path: QMessageBox.information(self, "导出完成", f"已导出 {self.tasks.export_csv(self.user.id, path)} 条任务")
    def clear(self):
        if QMessageBox.question(self, "二次确认", "确定清空自己的学习记录吗？此操作不可恢复。") == QMessageBox.StandardButton.Yes: self.tasks.clear_user_data(self.user.id); self.refresh(); self.on_changed()

