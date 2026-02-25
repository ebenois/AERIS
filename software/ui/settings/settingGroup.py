import sys
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QPushButton,
)
from PyQt6.QtCore import Qt, QSettings, pyqtSignal


class SettingGroup(QWidget):
    valueChanged = pyqtSignal(int)

    def __init__(self, name, min_val, max_val, current_val, reset_val):
        super().__init__()
        self.name = name
        self.reset_val = reset_val

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)

        self.label = QLabel(f"{self.name}: {current_val}px")
        layout.addWidget(self.label)

        controls_layout = QHBoxLayout()

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(current_val)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedWidth(60)

        controls_layout.addWidget(self.slider)
        controls_layout.addWidget(self.reset_btn)
        layout.addLayout(controls_layout)

        self.slider.valueChanged.connect(self._on_value_changed)
        self.reset_btn.clicked.connect(lambda: self.slider.setValue(self.reset_val))

    def _on_value_changed(self, value):
        self.label.setText(f"{self.name}: {value}px")
        self.valueChanged.emit(value)

    def setValue(self, value):
        self.slider.setValue(value)
