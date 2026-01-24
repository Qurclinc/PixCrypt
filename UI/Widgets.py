from PyQt5.QtWidgets import QPushButton, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HackButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Consolas", 10, QFont.Bold))
        self.setStyleSheet("""
            QPushButton {
                background-color: #001100;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #003300;
                border: 2px solid #00ff00;
            }
            QPushButton:pressed {
                background-color: #005500;
            }
            QPushButton:disabled {
                background-color: #000800;
                color: #008800;
                border: 2px solid #008800;
            }
        """)

class HackLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Consolas", 9))
        self.setStyleSheet("color: #00ff00;")
        self.setAlignment(Qt.AlignCenter)

class HackFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #000000;
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
            }
        """)