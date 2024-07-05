'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-05 17:00:58
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-05 17:30:14
FilePath: \aistore\app\threads\download_thread_test.py
Description: download_thread test
'''
import sys
import os
sys.path.insert(0, r'D:/aistore')
import tempfile
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from app.threads.download_thread import DownloadThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('文件下载')
        self.setGeometry(200, 200, 400, 200)

        self.btn_download = QPushButton('下载文件', self)
        self.btn_download.setGeometry(150, 80, 100, 30)
        self.btn_download.clicked.connect(self.start_download)

        self.progress_dialog = QProgressDialog(self)
        self.progress_dialog.setWindowTitle('下载进度')
        self.progress_dialog.setCancelButton(None)
        self.progress_dialog.setWindowModality(Qt.WindowModal)

    def start_download(self):
        self.download_thread = DownloadThread(url)
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.download_complete.connect(self.download_complete)
        self.download_thread.start()

        self.progress_dialog.setLabelText('正在下载...')
        self.progress_dialog.setRange(0, 100)
        self.progress_dialog.setValue(0)
        self.progress_dialog.exec_()

    def update_progress(self, percent):
        self.progress_dialog.setValue(percent)

    def download_complete(self, file_path):
        self.progress_dialog.reset()
        self.progress_dialog.hide()
        print(f"文件下载完成，保存在: {file_path}")


if __name__ == '__main__':
    url = 'http://183.232.235.52:7860/chfs/shared/facefusion/facefusion-1.0.0.zip'  # 替换为实际要下载的文件链接
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())