'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 17:09:31
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-28 16:06:04
FilePath: \aistore\test\test_database.py
Description: 
'''
import sys
sys.path.insert(0, r'D:/aistore')

from PyQt5.QtWidgets import QApplication
from app.database.ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
