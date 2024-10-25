from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QCheckBox, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import sys
from admin_dashboard import AdminDashboard
from tem_dashboard import TEMDashboard

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entry Manager")
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #222; color: #e0e0e0;")
        self.setWindowIcon(QIcon("logo.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

         # Create welcome label
        self.welcome_label = QLabel("Welcome to Darshan Management System")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

        # Create username and password fields
        self.username_label = QLabel("Username")
        self.username_label.setStyleSheet("font-size: 16px; font-family: Arial;")
        self.layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.username_input)

        self.password_label = QLabel("Password")
        self.password_label.setStyleSheet("font-size: 16px; font-family: Arial;")
        self.layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.password_input)

        # Create remember me checkbox and language selection dropdown
        self.remember_me_checkbox = QCheckBox("Remember Me")
        self.remember_me_checkbox.setStyleSheet("font-size: 14px; font-family: Arial;")
        self.layout.addWidget(self.remember_me_checkbox)

        self.language_label = QLabel("Language")
        self.language_label.setStyleSheet("font-size: 14px; font-family: Arial;")
        self.layout.addWidget(self.language_label)

        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(["English", "Spanish", "French"])
        self.language_dropdown.setStyleSheet("background-color: #1e1e1e; color: #e0e0e0; padding: 10px; border-radius: 5px;")
        self.layout.addWidget(self.language_dropdown)

        # Create login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #333; color: #e0e0e0; padding: 10px; border-radius: 5px; font-size: 16px; font-family: Arial;")
        self.login_button.clicked.connect(self.handle_login)
        self.layout.addWidget(self.login_button)

        # Create forgot password, create account, and guest login buttons
        self.forgot_password_button = QPushButton("Forgot Password")
        self.forgot_password_button.setStyleSheet("font-size: 14px; font-family: Arial; text-decoration: underline;")
        self.forgot_password_button.clicked.connect(self.handle_forgot_password)
        self.layout.addWidget(self.forgot_password_button)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.setStyleSheet("font-size: 14px; font-family: Arial; text-decoration: underline;")
        self.create_account_button.clicked.connect(self.handle_create_account)
        self.layout.addWidget(self.create_account_button)

        self.guest_login_button = QPushButton("Guest Login")
        self.guest_login_button.setStyleSheet("font-size: 14px; font-family: Arial; text-decoration: underline;")
        self.guest_login_button.clicked.connect(self.handle_guest_login)
        self.layout.addWidget(self.guest_login_button)

    def handle_login(self):
        # Animate login button
        self.animate_button(self.login_button)

        username = self.username_input.text()
        password = self.password_input.text()

        # Dummy credentials (replace with your authentication logic)
        if username == "admin" and password == "adminpass":
            self.open_admin_dashboard()
        elif username == "tem" and password == "tempass":
            self.open_tems_dashboard()
        else:
            self.show_error("Login Failed", "Invalid username or password.")

    def animate_button(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        animation.setDuration(100)
        animation.setStartValue(button.geometry())
        animation.setEndValue(button.geometry().adjusted(-5, -5, 5, 5))
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

    def open_admin_dashboard(self):
        self.close()
        self.admin_dashboard = AdminDashboard()
        self.admin_dashboard.show()

    def open_tems_dashboard(self):
        self.close()
        self.tems_dashboard = TEMDashboard()
        self.tems_dashboard.show()

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def handle_forgot_password(self):
        # Implement forgot password logic here
        pass

    def handle_create_account(self):
        # Implement create account logic here
        pass

    def handle_guest_login(self):
        # Implement guest login logic here
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())