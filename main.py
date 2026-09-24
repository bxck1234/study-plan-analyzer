import sys

from PySide6.QtWidgets import QApplication

from database.db import init_db
from ui.login_window import LoginWindow


STYLESHEET = """
* { font-family: 'Microsoft YaHei', 'Segoe UI'; font-size: 14px; }
QMainWindow, QWidget { background: #f5f7fb; color: #263238; }
#sidebar { background: #ffffff; border-right: 1px solid #e5e9f0; }
#brand { color: #2457c5; font-size: 17px; font-weight: 700; line-height: 1.5; padding-bottom: 18px; }
#nav { border: none; background: transparent; }
#nav::item { padding: 13px 12px; border-radius: 8px; color: #5f6b7a; }
#nav::item:selected { background: #eaf0ff; color: #2457c5; font-weight: 700; }
#logout { color: #7b8794; padding: 12px; }
#loginCard { background: white; border: 1px solid #e2e8f0; border-radius: 16px; }
.heroTitle { color: #1f3b72; font-size: 30px; font-weight: 700; }
.heroSub { color: #61708a; font-size: 20px; line-height: 1.8; }
#sectionTitle, .sectionTitle { font-size: 19px; font-weight: 700; color: #1f2937; }
.pageTitle { font-size: 26px; font-weight: 700; color: #1f2937; padding-bottom: 8px; }
#topTitle { color: #526174; font-size: 14px; }
#userBadge { background: #eaf0ff; color: #2457c5; padding: 8px 14px; border-radius: 16px; }
#statCard { background: white; border: 1px solid #e4e9f2; border-radius: 12px; }
#statValue { color: #2457c5; font-size: 24px; font-weight: 700; }
#muted, .muted { color: #7a8797; }
#advice { background: #eef5ff; border-radius: 10px; padding: 14px; color: #36547c; }
QLineEdit, QComboBox, QSpinBox, QTimeEdit, QDateEdit, QTextEdit { background: white; border: 1px solid #d8e0eb; border-radius: 7px; padding: 8px; }
QPushButton { background: white; border: 1px solid #d4dce8; border-radius: 7px; padding: 8px 14px; }
QPushButton:hover { background: #f0f5ff; }
#primaryButton { background: #2f65d9; color: white; border: none; font-weight: 700; padding: 10px; }
#linkButton { border: none; color: #2f65d9; background: transparent; }
QTableWidget { background: white; border: 1px solid #e0e6ef; border-radius: 8px; gridline-color: #edf0f5; }
QHeaderView::section { background: #f7f9fc; border: none; padding: 9px; color: #637083; }
QListWidget { background: white; border: 1px solid #e4e9f2; border-radius: 10px; }
QListWidget::item { padding: 14px; border-bottom: 1px solid #f0f2f6; }
"""


def main():
    init_db(); app = QApplication(sys.argv); app.setStyleSheet(STYLESHEET); window = LoginWindow(); window.show(); sys.exit(app.exec())


if __name__ == "__main__": main()

