from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QDateEdit, QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QSpinBox, QTimeEdit, QVBoxLayout


SUBJECTS = ["数学", "语文", "英语", "物理", "化学", "生物", "政治", "历史", "地理", "其他"]
TASK_TYPES = ["作业", "刷题", "复习", "预习", "背诵", "错题整理", "阅读", "其他"]


def combo(items: list[str]) -> QComboBox:
    w = QComboBox(); w.addItems(items); return w


def info(parent, title: str, text: str): QMessageBox.information(parent, title, text)
def error(parent, text: str): QMessageBox.warning(parent, "提示", text)


class TaskDialog(QDialog):
    def __init__(self, parent=None, task: dict | None = None, suggestion: str | None = None, user_id: int | None = None):
        super().__init__(parent); self.setWindowTitle("编辑学习任务" if task else "新建学习任务"); self.setMinimumWidth(430)
        form = QFormLayout(self); self.date = QDateEdit(); self.date.setCalendarPopup(True); self.date.setDisplayFormat("yyyy-MM-dd"); self.date.setDate(__import__('PySide6').QtCore.QDate.currentDate())
        self.subject = combo(SUBJECTS); self.name = QLineEdit(); self.kind = combo(TASK_TYPES); self.start = QTimeEdit(); self.start.setDisplayFormat("HH:mm"); self.duration = QSpinBox(); self.duration.setRange(1, 1440); self.duration.setValue(45); self.difficulty = combo(["简单", "一般", "困难"]); self.priority = combo(["低", "中", "高"]); self.status = combo(["待完成", "进行中", "已完成", "延期"]); self.notes = QLineEdit()
        for label, widget in [("日期", self.date), ("科目", self.subject), ("任务名称", self.name), ("任务类型", self.kind), ("计划开始", self.start), ("计划时长(分钟)", self.duration), ("难度", self.difficulty), ("优先级", self.priority), ("状态", self.status), ("备注", self.notes)]: form.addRow(label, widget)
        self.suggestion_label = QLabel(suggestion or "暂无足够历史记录"); self.suggestion_label.setObjectName("muted"); form.addRow("历史推荐", self.suggestion_label)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel); buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); form.addRow(buttons)
        if user_id:
            from services.recommendation_service import RecommendationService
            def update_suggestion():
                self.suggestion_label.setText(RecommendationService().suggest_duration(user_id, self.subject.currentText(), self.kind.currentText(), self.difficulty.currentText()) or "暂无足够历史记录")
            self.subject.currentTextChanged.connect(update_suggestion); self.kind.currentTextChanged.connect(update_suggestion); self.difficulty.currentTextChanged.connect(update_suggestion); update_suggestion()
        if task:
            self.date.setDate(__import__('PySide6').QtCore.QDate.fromString(task["task_date"], "yyyy-MM-dd")); self.subject.setCurrentText(task["subject"]); self.name.setText(task["task_name"]); self.kind.setCurrentText(task["task_type"]); self.start.setTime(__import__('PySide6').QtCore.QTime.fromString(task["planned_start_time"], "HH:mm")); self.duration.setValue(task["planned_duration"]); self.difficulty.setCurrentText(task["difficulty"]); self.priority.setCurrentText(task["priority"]); self.status.setCurrentText(task["status"]); self.notes.setText(task["notes"] or "")

    def data(self) -> dict:
        return {"task_date": self.date.date().toString("yyyy-MM-dd"), "subject": self.subject.currentText(), "task_name": self.name.text().strip(), "task_type": self.kind.currentText(), "planned_start_time": self.start.time().toString("HH:mm"), "planned_duration": self.duration.value(), "difficulty": self.difficulty.currentText(), "priority": self.priority.currentText(), "status": self.status.currentText(), "notes": self.notes.text().strip()}
