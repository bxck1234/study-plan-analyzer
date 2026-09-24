from datetime import datetime
from PySide6.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QTextEdit, QVBoxLayout, QWidget
from services.task_service import TaskService


class ExecutionPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__(); self.user_id = user_id; self.service = TaskService(); layout = QVBoxLayout(self); title = QLabel("执行记录"); title.setObjectName("pageTitle"); layout.addWidget(title); self.task = QComboBox(); layout.addWidget(self.task); form = QFormLayout(); self.start = QLineEdit(); self.start.setPlaceholderText("例如 19:00"); self.end = QLineEdit(); self.end.setPlaceholderText("例如 19:50，可留空"); self.duration = QSpinBox(); self.duration.setRange(0, 1440); self.duration.setValue(45); self.level = QComboBox(); self.level.addItems(["未完成", "部分完成", "基本完成", "完全完成"]); self.completed = QComboBox(); self.completed.addItems(["否", "是"]); self.interrupted = QComboBox(); self.interrupted.addItems(["否", "是"]); self.evaluation = QSpinBox(); self.evaluation.setRange(1, 5); self.evaluation.setValue(3); self.notes = QTextEdit(); self.notes.setMaximumHeight(75)
        for label, w in [("实际开始时间", self.start), ("实际结束时间", self.end), ("实际学习时长(分钟)", self.duration), ("完成程度", self.level), ("是否完成", self.completed), ("是否受到干扰", self.interrupted), ("自我评价(1-5)", self.evaluation), ("备注", self.notes)]: form.addRow(label, w)
        layout.addLayout(form); save = QPushButton("保存执行记录"); save.setObjectName("primaryButton"); save.clicked.connect(self.save); layout.addWidget(save); layout.addStretch(); self.refresh()

    def refresh(self):
        self.task.clear(); rows = self.service.list_tasks(self.user_id)
        for r in rows: self.task.addItem(f"{r['task_date']} · {r['subject']} · {r['task_name']}", r["id"])

    def save(self):
        if self.task.currentIndex() < 0: QMessageBox.warning(self, "提示", "请先创建学习计划"); return
        actual = self.duration.value(); start, end = self.start.text().strip(), self.end.text().strip()
        if start and end:
            try: actual = int((datetime.strptime(end, "%H:%M") - datetime.strptime(start, "%H:%M")).seconds / 60)
            except ValueError: QMessageBox.warning(self, "提示", "时间格式应为 HH:MM"); return
        data = {"actual_start_time": start, "actual_end_time": end, "actual_duration": actual, "completion_level": self.level.currentText(), "completed": self.completed.currentText() == "是" or self.level.currentText() == "完全完成", "interrupted": self.interrupted.currentText() == "是", "self_evaluation": self.evaluation.value(), "notes": self.notes.toPlainText().strip()}
        self.service.save_execution(self.user_id, self.task.currentData(), data); QMessageBox.information(self, "保存成功", "执行记录已保存"); self.refresh()

