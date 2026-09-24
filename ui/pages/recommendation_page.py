from PySide6.QtWidgets import QLabel, QListWidget, QVBoxLayout, QWidget
from services.recommendation_service import RecommendationService


class RecommendationPage(QWidget):
    def __init__(self, user_id: int):
        super().__init__(); self.user_id = user_id; layout = QVBoxLayout(self); title = QLabel("学习建议"); title.setObjectName("pageTitle"); layout.addWidget(title); intro = QLabel("建议来自你的历史计划与执行记录，不会预先写入演示数据。\n记录越完整，建议越具体。"); intro.setObjectName("muted"); layout.addWidget(intro); self.list = QListWidget(); layout.addWidget(self.list); layout.addStretch(); self.refresh()
    def refresh(self): self.list.clear(); self.list.addItems(["• " + x for x in RecommendationService().get_recommendations(self.user_id)])

