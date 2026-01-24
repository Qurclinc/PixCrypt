import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from UI.Widgets import HackLabel
from UI.CryptoTab import CryptoTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PixCrypt v1.0")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("background-color: #000000;")
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = HackLabel("PixCrypt", self)
        header.setFont(QFont("Consolas", 16, QFont.Bold))
        header.setStyleSheet("color: #00ff00; border: 2px solid #00ff00; padding: 10px;")
        layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #00ff00;
                background-color: #000000;
            }
            QTabBar::tab {
                background-color: #001100;
                color: #00ff00;
                padding: 8px 16px;
                border: 1px solid #00ff00;
                font-family: Consolas;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #003300;
            }
            QTabBar::tab:hover {
                background-color: #002200;
            }
        """)
        
        # Create tabs
        encrypt_tab = CryptoTab("encrypt")
        decrypt_tab = CryptoTab("decrypt")
        
        tabs.addTab(encrypt_tab, "ENCRYPT")
        tabs.addTab(decrypt_tab, "DECRYPT")
        
        layout.addWidget(tabs)