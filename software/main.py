import sys
import ctypes
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QIcon

size = 600

try:
    myappid = 'AERIS'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

app = QApplication(sys.argv)

window = QWidget()
window.setWindowIcon(QIcon("software/assets/logo.png"))
window.setWindowTitle("AERIS")
window.resize(size, size)
window.show() 

app.exec()
