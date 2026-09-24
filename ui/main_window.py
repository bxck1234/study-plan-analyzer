from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QMainWindow, QStackedWidget, QVBoxLayout, QWidget

from ui.pages.analysis_page import AnalysisPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.execution_page import ExecutionPage
from ui.pages.plan_page import PlanPage
from ui.pages.profile_page import ProfilePage
from ui.pages.recommendation_page import RecommendationPage


class MainWindow(QMainWindow):
    def __init__(self, user, login_window):
        super().__init__(); self.user = user; self.login_window = login_window; self.setWindowTitle("个人学习计划执行偏差分析工具"); self.resize(1180, 760); root = QWidget(); layout = QHBoxLayout(root); layout.setContentsMargins(0, 0, 0, 0); sidebar = QWidget(); sidebar.setObjectName("sidebar"); side = QVBoxLayout(sidebar); side.setContentsMargins(20, 24, 20, 20); brand = QLabel("StudyPlanAnalyzer\n学习计划执行偏差分析"); brand.setObjectName("brand"); side.addWidget(brand); self.nav = QListWidget(); self.nav.setObjectName("nav"); [self.nav.addItem(QListWidgetItem(x)) for x in ["首页", "学习计划", "执行记录", "数据分析", "学习建议", "我的"]]; self.nav.currentRowChanged.connect(self.switch_page); side.addWidget(self.nav); logout = QLabel("退出登录"); logout.setObjectName("logout"); logout.setCursor(Qt.CursorShape.PointingHandCursor); logout.mousePressEvent = lambda e: self.logout(); side.addWidget(logout); layout.addWidget(sidebar); content = QWidget(); cl = QVBoxLayout(content); cl.setContentsMargins(28, 24, 28, 24); head = QHBoxLayout(); head.addWidget(QLabel("个人学习成长空间", objectName="topTitle")); head.addStretch(); self.user_label = QLabel(user.nickname); self.user_label.setObjectName("userBadge"); head.addWidget(self.user_label); cl.addLayout(head); self.stack = QStackedWidget(); self.pages = [DashboardPage(user.id), PlanPage(user.id), ExecutionPage(user.id), AnalysisPage(user.id), RecommendationPage(user.id), ProfilePage(user, self.update_user_label)]; [self.stack.addWidget(p) for p in self.pages]; cl.addWidget(self.stack); layout.addWidget(content, 1); self.setCentralWidget(root); self.nav.setCurrentRow(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index); page = self.pages[index]; getattr(page, "refresh", lambda: None)()
    def update_user_label(self): self.user_label.setText(self.user.nickname); self.pages[0].refresh(); self.pages[4].refresh()
    def logout(self): self.close(); self.login_window.show_login()

