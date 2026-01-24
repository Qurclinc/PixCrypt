# from Services.Crypter import Crypter

# cr = Crypter()


# cr.set_key("./cxder.jpg")
# # response = cr.encrypt("./Качьянов_В_Д_23КБсРЗПО_2_Реш_лин_ур_ий.docx", "./Качьянов.crypted")
# response = cr.decrypt("./Качьянов.crypted", "./dec.docx")
# print(response)

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor

from UI.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0))
    palette.setColor(QPalette.WindowText, QColor(0, 255, 0))
    palette.setColor(QPalette.Base, QColor(0, 0, 0))
    palette.setColor(QPalette.AlternateBase, QColor(0, 20, 0))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 255, 0))
    palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))
    palette.setColor(QPalette.Text, QColor(0, 255, 0))
    palette.setColor(QPalette.Button, QColor(0, 20, 0))
    palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Highlight, QColor(0, 100, 0))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())