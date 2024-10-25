from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from utils import scan_qr_from_camera, fetch_customer_data

class TEMDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ticket Entry Manager Dashboard")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Apply stylesheet
        stylesheet = """
        QMainWindow {
            background-color: #121212;
        }

        QWidget {
            background-color: #1e1e1e;
        }

        QLabel {
            color: #e0e0e0;
            font-size: 21\px;
        }

        QPushButton {
            background-color: #333;
            color: #e0e0e0;
            border: 1px solid #444;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }

        QPushButton:hover {
            background-color: #444;
        }

        QPushButton:pressed {
            background-color: #555;
        }

        QVBoxLayout {
            margin: 20px;
        }

        QLabel#header_label {
            font-size: 32px;
            font-weight: bold;
            color: #e0e0e0;
        }

        """
        self.setStyleSheet(stylesheet)


        # Create a header
        self.header_label = QLabel("Welcome to the Ticket Entry Manager")
        self.header_label.setObjectName("header_label")
        self.layout.addWidget(self.header_label)

        # Create scan button
        self.scan_button = QPushButton("Scan QR Code")
        self.scan_button.setIcon(QIcon('scan_icon.png'))  # Add an icon if you have one
        self.scan_button.clicked.connect(self.scan_qr_code)
        self.layout.addWidget(self.scan_button)

        # Create result label
        self.result_label = QLabel("Result will be displayed here")
        self.result_label.setObjectName("result_label")
        self.layout.addWidget(self.result_label)

        # Create footer
        self.footer_label = QLabel("© 2024 AutoMates")
        self.footer_label.setObjectName("footer_label")
        self.layout.addWidget(self.footer_label)

    def scan_qr_code(self):
        customer_id = scan_qr_from_camera()
        if customer_id:
            data = fetch_customer_data(customer_id)
            if data:
                result_text = "\n".join(f"{key}: {value}" for key, value in data.items())
            else:
                result_text = "No data found for the given customer ID."
            self.result_label.setText(result_text)
        else:
            self.result_label.setText("QR code scanning failed.")
            self.show_error("Error", "QR code scanning failed. Please try again.")

    def show_error(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TEMDashboard()
    window.show()
    sys.exit(app.exec_())
