'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:57:37
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-27 17:08:58
FilePath: \aistore\app\database\main.py
Description: 
'''
import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
