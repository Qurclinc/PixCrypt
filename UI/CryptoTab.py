import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from UI.Widgets import HackButton, HackLabel, HackFrame
from UI.Dialogs import SuccessWindow, CriticalWindow
from Services.Crypter import Crypter

class CryptoTab(QWidget):
    def __init__(self, mode="encrypt", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.crypter = Crypter()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = HackLabel(f"{self.mode.upper()} FILE", self)
        title.setFont(QFont("Consolas", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Source file selection
        source_frame = HackFrame(self)
        source_layout = QVBoxLayout(source_frame)
        
        source_layout.addWidget(HackLabel("SOURCE FILE:"))
        self.source_btn = HackButton("Select File", self)
        self.source_btn.clicked.connect(self.select_source_file)
        source_layout.addWidget(self.source_btn)
        
        self.source_label = HackLabel("No file selected", self)
        source_layout.addWidget(self.source_label)
        
        layout.addWidget(source_frame)
        
        # Key file selection
        key_frame = HackFrame(self)
        key_layout = QVBoxLayout(key_frame)
        
        key_layout.addWidget(HackLabel("ENCRYPTION KEY (PNG/JPG):"))
        self.key_btn = HackButton("Select Key", self)
        self.key_btn.clicked.connect(self.select_key_file)
        self.key_btn.setEnabled(False)
        key_layout.addWidget(self.key_btn)
        
        self.key_label = HackLabel("No key selected", self)
        key_layout.addWidget(self.key_label)
        
        layout.addWidget(key_frame)
        
        # Action button
        self.action_btn = HackButton(f"{self.mode.upper()}", self)
        self.action_btn.clicked.connect(self.perform_action)
        self.action_btn.setEnabled(False)
        layout.addWidget(self.action_btn)
        
        # Status
        self.status_label = HackLabel("Ready...", self)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
        
    def select_source_file(self):
        if self.mode == "encrypt":
            file_filter = "All Files (*)"
        else:
            file_filter = "Encrypted Files (*.enc)"
            
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Source File", "", file_filter)
        if file_path:
            self.source_file = file_path
            self.source_label.setText(os.path.basename(file_path))
            self.key_btn.setEnabled(True)
            self.update_action_button()
            
    def select_key_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Key Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            try:
                self.crypter.set_key(file_path)
                self.key_file = file_path
                self.key_label.setText(os.path.basename(file_path))
                self.update_action_button()
            except Exception as e:
                CriticalWindow(f"Invalid key file: {str(e)}").exec()
                
    def update_action_button(self):
        if hasattr(self, 'source_file') and hasattr(self, 'key_file'):
            self.action_btn.setEnabled(True)
            
    def perform_action(self):
        if self.mode == "encrypt":
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Encrypted File", "", "Encrypted Files (*.enc)")
        else:
            output_path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted File", "", "All Files (*)")
            
        if output_path:
            if self.mode == "encrypt":
                result = self.crypter.encrypt(self.source_file, output_path)
            else:
                result = self.crypter.decrypt(self.source_file, output_path)
                
            if result[0]:  # Success
                SuccessWindow(result[1]).exec()
                self.status_label.setText("Operation completed successfully")
            else:
                CriticalWindow(result[1]).exec()
                self.status_label.setText("Operation failed")