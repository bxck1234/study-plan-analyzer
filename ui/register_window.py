from PySide6.QtWidgets import QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget, QMainWindow
from services.auth_service import AuthService


class RegisterWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__(); self.login_window = login_window; self.auth = AuthService(); self.setWindowTitle("注册新账号"); self.setMinimumSize(520, 440)
        root = QWidget(); layout = QVBoxLayout(root); layout.setContentsMargins(55, 45, 55, 45); title = QLabel("创建你的学习账户"); title.setObjectName("sectionTitle"); layout.addWidget(title); form = QFormLayout(); self.username = QLineEdit(); self.nickname = QLineEdit(); self.password = QLineEdit(); self.password.setEchoMode(QLineEdit.EchoMode.Password); self.confirm = QLineEdit(); self.confirm.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("用户名", self.username); form.addRow("昵称", self.nickname); form.addRow("密码", self.password); form.addRow("再次输入", self.confirm); layout.addLayout(form); hint = QLabel("用户名至少3个字符，密码至少6位"); hint.setObjectName("muted"); layout.addWidget(hint); submit = QPushButton("注册"); submit.setObjectName("primaryButton"); submit.clicked.connect(self.submit); back = QPushButton("返回登录"); back.setObjectName("linkButton"); back.clicked.connect(self.back); layout.addWidget(submit); layout.addWidget(back); layout.addStretch(); self.setCentralWidget(root)

    def submit(self):
        u, n, p, c = self.username.text().strip(), self.nickname.text().strip(), self.password.text(), self.confirm.text()
        if len(u) < 3: QMessageBox.warning(self, "提示", "用户名长度至少3个字符"); return
        if not n: QMessageBox.warning(self, "提示", "昵称不能为空"); return
        if len(p) < 6: QMessageBox.warning(self, "提示", "密码至少6位"); return
        if p != c: QMessageBox.warning(self, "提示", "两次密码不一致"); return
        ok, msg = self.auth.register(u, n, p); QMessageBox.information(self, "提示", msg) if ok else QMessageBox.warning(self, "提示", msg)
        if ok: self.back()

    def back(self): self.close(); self.login_window.show()

