import sys
sys.path.insert(0, r'D:/aistore')

from PyQt5.QtWidgets import QApplication
from app.database.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
