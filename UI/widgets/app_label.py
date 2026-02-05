from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AppLabel(QLabel):
    def __init__(
        self,
        text="",
        parent=None,
        align=Qt.AlignLeft,
        size=9,
        bold=False
    ):
        super().__init__(text, parent)

        self.setFont(
            QFont(
                "Consolas",
                size,
                QFont.Bold if bold else QFont.Normal
            )
        )

        if align is not None:
            self.setAlignment(align)
