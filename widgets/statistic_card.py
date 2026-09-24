from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatisticCard(QFrame):
    def __init__(self, title: str, value: str = "0"):
        super().__init__(); self.setObjectName("statCard")
        layout = QVBoxLayout(self); layout.setContentsMargins(18, 14, 18, 14)
        self.title = QLabel(title); self.title.setObjectName("muted")
        self.value = QLabel(value); self.value.setObjectName("statValue")
        layout.addWidget(self.title); layout.addWidget(self.value)

    def set_value(self, value: str): self.value.setText(value)

