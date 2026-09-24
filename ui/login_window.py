from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget

from services.auth_service import AuthService
from ui.register_window import RegisterWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.auth = AuthService(); self.main_window = None; self.setWindowTitle("个人学习计划执行偏差分析工具"); self.setMinimumSize(900, 560)
        root = QWidget(); outer = QHBoxLayout(root); outer.setContentsMargins(60, 45, 60, 45); outer.setSpacing(70)
        left = QVBoxLayout(); title = QLabel("学习计划执行偏差分析工具"); title.setObjectName("heroTitle"); left.addWidget(title); sub = QLabel("了解计划\n记录执行\n发现偏差\n持续改进"); sub.setObjectName("heroSub"); left.addWidget(sub); left.addStretch(); outer.addLayout(left, 1)
        card = QFrame(); card.setObjectName("loginCard"); form = QVBoxLayout(card); form.setContentsMargins(35, 30, 35, 30); welcome = QLabel("欢迎回来"); welcome.setObjectName("sectionTitle"); form.addWidget(welcome); form.addSpacing(15)
        self.username = QLineEdit(); self.username.setPlaceholderText("用户名"); self.password = QLineEdit(); self.password.setPlaceholderText("密码"); self.password.setEchoMode(QLineEdit.EchoMode.Password); form.addWidget(self.username); form.addWidget(self.password)
        row = QHBoxLayout(); self.remember = QCheckBox("记住用户名"); toggle = QPushButton("显示密码"); toggle.setObjectName("linkButton"); toggle.clicked.connect(lambda: self.password.setEchoMode(QLineEdit.EchoMode.Normal if self.password.echoMode() == QLineEdit.EchoMode.Password else QLineEdit.EchoMode.Password)); row.addWidget(self.remember); row.addStretch(); row.addWidget(toggle); form.addLayout(row)
        login = QPushButton("登录"); login.setObjectName("primaryButton"); login.clicked.connect(self.do_login); form.addWidget(login); register = QPushButton("还没有账号？  注册新账号"); register.setObjectName("linkButton"); register.clicked.connect(self.open_register); form.addWidget(register); form.addStretch(); outer.addWidget(card, 1); self.setCentralWidget(root)

    def do_login(self):
        user = self.auth.login(self.username.text().strip(), self.password.text())
        if not user: QMessageBox.warning(self, "登录失败", "用户名或密码错误"); return
        from ui.main_window import MainWindow
        self.main_window = MainWindow(user, self); self.main_window.show(); self.hide()

    def open_register(self):
        self.register_window = RegisterWindow(self); self.register_window.show(); self.hide()

    def show_login(self): self.show(); self.username.setFocus()

