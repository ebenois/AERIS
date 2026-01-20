from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AIWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AI"))
