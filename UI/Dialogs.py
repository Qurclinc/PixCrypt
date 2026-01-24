from PyQt5.QtWidgets import QMessageBox

class SuccessWindow(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("SUCCESS")
        self.setText(message)
        self.setStyleSheet("""
            QMessageBox {
                background-color: #000000;
                color: #00ff00;
            }
            QMessageBox QLabel {
                color: #00ff00;
                font-family: Consolas;
            }
            QMessageBox QPushButton {
                background-color: #001100;
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 5px 15px;
                font-family: Consolas;
            }
        """)

class CriticalWindow(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("ERROR")
        self.setText(message)
        self.setIcon(QMessageBox.Critical)
        self.setStyleSheet("""
            QMessageBox {
                background-color: #000000;
                color: #ff0000;
            }
            QMessageBox QLabel {
                color: #ff0000;
                font-family: Consolas;
            }
            QMessageBox QPushButton {
                background-color: #110000;
                color: #ff0000;
                border: 1px solid #ff0000;
                padding: 5px 15px;
                font-family: Consolas;
            }
        """)