from PySide2.QtWidgets import QPushButton, QApplication
from mainwindow import MainWindow
import sys

# Aplicación de Qt
app = QApplication()
window = MainWindow()
window.show()
# Qt loop
sys.exit(app.exec_())