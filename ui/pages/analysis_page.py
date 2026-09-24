from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from services.analysis_service import get_subject_statistics, get_task_type_statistics, get_time_period_statistics, get_recent_trend
from widgets.charts import AnalysisChart


class AnalysisPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__(); self.user_id = user_id; layout = QVBoxLayout(self); title = QLabel("数据分析"); title.setObjectName("pageTitle"); layout.addWidget(title); self.kind = QComboBox(); self.kind.addItems(["科目分析", "任务类型分析", "时间段分析", "最近7天趋势", "最近30天偏差趋势"]); self.kind.currentIndexChanged.connect(self.refresh); layout.addWidget(self.kind); self.summary = QLabel(); self.summary.setObjectName("muted"); layout.addWidget(self.summary); self.table = QTableWidget(); layout.addWidget(self.table); self.chart = AnalysisChart(); layout.addWidget(self.chart); self.refresh()

    def refresh(self):
        idx = self.kind.currentIndex()
        if idx == 0: rows = get_subject_statistics(self.user_id); headers = ["科目", "任务数", "平均计划", "平均实际", "平均偏差", "偏差率", "完成率"]; values = [[r["name"], r["count"], f"{r['avg_planned']:.0f} min", f"{r['avg_actual']:.0f} min", f"{r['avg_deviation']:+.0f} min", f"{r['avg_rate']:+.1f}%", f"{r['completion_rate']:.1f}%"] for r in rows]
        elif idx == 1: rows = get_task_type_statistics(self.user_id); headers = ["任务类型", "任务数", "平均计划", "平均实际", "偏差率", "完成率"]; values = [[r["name"], r["count"], f"{r['avg_planned']:.0f} min", f"{r['avg_actual']:.0f} min", f"{r['avg_rate']:+.1f}%", f"{r['completion_rate']:.1f}%"] for r in rows]
        elif idx == 2: rows = get_time_period_statistics(self.user_id); headers = ["时间段", "任务数", "完成率", "平均偏差率", "完全完成比例"]; values = [[r["name"], r["count"], f"{r['completion_rate']:.1f}%", f"{r['avg_rate']:+.1f}%", f"{r['complete_rate']:.1f}%"] for r in rows]
        elif idx == 3: rows = get_recent_trend(self.user_id, 7); headers = ["日期", "计划分钟", "实际分钟", "完成率", "平均偏差率"]; values = [[r["date"], r["planned"], r["actual"], f"{r['completion_rate']:.1f}%", f"{r['avg_rate']:+.1f}%"] for r in rows]; self.summary.setText("最近7天计划时长与实际时长趋势（数据来自你的执行记录）")
        else: rows = get_recent_trend(self.user_id, 30); headers = ["日期", "计划分钟", "实际分钟", "完成率", "平均偏差率"]; values = [[r["date"], r["planned"], r["actual"], f"{r['completion_rate']:.1f}%", f"{r['avg_rate']:+.1f}%"] for r in rows]; self.summary.setText("最近30天平均偏差率变化趋势")
        if idx not in (3, 4): self.summary.setText("统计结果仅基于当前账号的真实记录；负偏差需结合完成程度理解。")
        self.table.setColumnCount(len(headers)); self.table.setHorizontalHeaderLabels(headers); self.table.setRowCount(len(values))
        for i, row in enumerate(values):
            for j, v in enumerate(row): self.table.setItem(i, j, QTableWidgetItem(str(v)))
        if idx == 0: self.chart.draw("各科平均偏差率", [r["name"] for r in rows], [r["avg_rate"] for r in rows])
        elif idx == 1: self.chart.draw("各任务类型平均偏差率", [r["name"] for r in rows], [r["avg_rate"] for r in rows])
        elif idx == 2: self.chart.draw("不同时间段完成率", [r["name"] for r in rows], [r["completion_rate"] for r in rows])
        elif idx == 3: self.chart.draw("最近7天计划与实际学习时间", [r["date"][5:] for r in rows], [r["planned"] for r in rows], "line", [r["actual"] for r in rows])
        else: self.chart.draw("最近30天平均偏差率变化", [r["date"][5:] for r in rows], [r["avg_rate"] for r in rows], "line")
