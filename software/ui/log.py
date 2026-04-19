from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class LogWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ici, il y aura les instructions de l'assistant"))
