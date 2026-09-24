from PySide6.QtWidgets import QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from services.analysis_service import get_daily_summary
from services.recommendation_service import RecommendationService
from widgets.statistic_card import StatisticCard


class DashboardPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__(); self.user_id = user_id; layout = QVBoxLayout(self); title = QLabel("首页"); title.setObjectName("pageTitle"); layout.addWidget(title); cards = QHBoxLayout(); self.cards = [StatisticCard(x) for x in ["今日计划", "今日完成", "今日完成率", "今日平均偏差"]]; [cards.addWidget(c) for c in self.cards]; layout.addLayout(cards); layout.addWidget(QLabel("今日任务", objectName="sectionTitle")); self.table = QTableWidget(0, 5); self.table.setHorizontalHeaderLabels(["科目", "任务", "计划开始", "计划时长", "状态"]); self.table.horizontalHeader().setStretchLastSection(True); layout.addWidget(self.table); layout.addWidget(QLabel("今日学习建议", objectName="sectionTitle")); self.advice = QLabel(); self.advice.setWordWrap(True); self.advice.setObjectName("advice"); layout.addWidget(self.advice); layout.addStretch(); self.refresh()

    def refresh(self):
        data = get_daily_summary(self.user_id); self.cards[0].set_value(str(data["planned_count"])); self.cards[1].set_value(str(data["completed_count"])); self.cards[2].set_value(f"{data['completion_rate']:.1f}%"); self.cards[3].set_value(f"{data['avg_deviation']:+.1f}%"); rows = data["tasks"]; self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for j, v in enumerate([r["subject"], r["task_name"], r["planned_start_time"], f"{r['planned_duration']} 分钟", r["status"]]): self.table.setItem(i, j, QTableWidgetItem(str(v)))
        self.advice.setText("\n".join("• " + x for x in RecommendationService().get_recommendations(self.user_id)[:2]))

