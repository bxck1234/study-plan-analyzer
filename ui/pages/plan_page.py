from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from services.task_service import TaskService
from services.recommendation_service import RecommendationService
from ui.base import SUBJECTS, TaskDialog


class PlanPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__(); self.user_id = user_id; self.service = TaskService(); layout = QVBoxLayout(self); top = QHBoxLayout(); title = QLabel("学习计划"); title.setObjectName("pageTitle"); top.addWidget(title); top.addStretch(); add = QPushButton("＋ 新建任务"); add.setObjectName("primaryButton"); add.clicked.connect(self.add_task); top.addWidget(add); layout.addLayout(top); filters = QHBoxLayout(); self.search = QLineEdit(); self.search.setPlaceholderText("搜索任务或科目"); self.date_filter = QLineEdit(); self.date_filter.setPlaceholderText("日期 YYYY-MM-DD"); self.subject = QComboBox(); self.subject.addItems(["全部科目"] + SUBJECTS); self.status = QComboBox(); self.status.addItems(["全部状态", "待完成", "进行中", "已完成", "延期"]); refresh = QPushButton("筛选"); refresh.clicked.connect(self.refresh); [filters.addWidget(x) for x in [self.search, self.date_filter, self.subject, self.status, refresh]]; layout.addLayout(filters); self.table = QTableWidget(0, 9); self.table.setHorizontalHeaderLabels(["日期", "科目", "任务", "类型", "开始", "计划分钟", "难度", "优先级", "状态"]); self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); layout.addWidget(self.table); actions = QHBoxLayout(); edit = QPushButton("编辑选中"); edit.clicked.connect(self.edit_task); delete = QPushButton("删除选中"); delete.clicked.connect(self.delete_task); [actions.addWidget(x) for x in [edit, delete]]; actions.addStretch(); layout.addLayout(actions); self.refresh()

    def selected_id(self):
        row = self.table.currentRow(); return int(self.table.item(row, 0).data(32)) if row >= 0 and self.table.item(row, 0) else None

    def refresh(self):
        rows = self.service.list_tasks(self.user_id, self.search.text().strip(), task_date=self.date_filter.text().strip(), subject=self.subject.currentText(), status=self.status.currentText()); self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            vals = [r["task_date"], r["subject"], r["task_name"], r["task_type"], r["planned_start_time"], r["planned_duration"], r["difficulty"], r["priority"], r["status"]]
            for j, v in enumerate(vals): self.table.setItem(i, j, QTableWidgetItem(str(v)))
            self.table.item(i, 0).setData(32, r["id"])

    def add_task(self):
        d = TaskDialog(self, user_id=self.user_id); d.accepted.connect(lambda: self._save(d)); d.exec()
    def _save(self, d, task_id=None):
        data = d.data()
        if not data["task_name"]: QMessageBox.warning(self, "提示", "任务名称不能为空"); return
        self.service.save_task(self.user_id, data, task_id); self.refresh()
    def edit_task(self):
        tid = self.selected_id()
        if not tid: return
        task = self.service.get_task(self.user_id, tid); d = TaskDialog(self, task, user_id=self.user_id); d.accepted.connect(lambda: self._save(d, tid)); d.exec()
    def delete_task(self):
        tid = self.selected_id()
        if not tid: return
        if QMessageBox.question(self, "确认删除", "确定删除选中的任务及其执行记录吗？") == QMessageBox.StandardButton.Yes: self.service.delete_task(self.user_id, tid); self.refresh()
