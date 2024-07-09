import sys
import tempfile
import requests
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MessageBox
# import ptvsd
from app.common.config import VERSION,UPDATE_INFO_URL

from app.common.logger import logger
from packaging import version

import sys
import os
import tempfile
import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qfluentwidgets import (MessageBoxBase,SubtitleLabel,ProgressBar,ProgressRing)
from app.threads.download_thread import DownloadThread

class UpdateChecker(QThread):
    update_found = pyqtSignal(dict)
    no_update_found = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)

    def run(self):
        # ptvsd.debug_this_thread()
        try:
            response = requests.get(UPDATE_INFO_URL)
            if response.status_code == 200:
                latest_version_info = response.json()
                latest_version = latest_version_info['version']

                if version.parse(latest_version) > version.parse(VERSION):
                    self.update_found.emit(latest_version_info)
                else:
                    self.no_update_found.emit()
            else:
                self.error_occurred.emit(f"Failed to check for updates: {response.status_code}")
        except Exception as e:
            self.error_occurred.emit(str(e))

class UpdateManager(QObject):
    update_available = pyqtSignal(dict)
    no_update_available = pyqtSignal()
    update_error = pyqtSignal(str)

    def __init__(self, main_window, start_up = False):
        super().__init__()

        self.main_window = main_window
        self.update_checker_thread = UpdateChecker(parent=self)
        self.download_thread = None
        self.start_up = start_up
        
        self.progress_window = None
        self.connectSignalToSlot()

    def connectSignalToSlot(self):
        self.update_checker_thread.update_found.connect(self.update_available.emit)
        self.update_checker_thread.no_update_found.connect(self.no_update_available.emit)
        self.update_checker_thread.error_occurred.connect(self.update_error.emit)

        # Connect update manager signals to appropriate slots
        self.update_available.connect(self.notify_update_found)
        self.no_update_available.connect(self.notify_no_update_found)
        self.update_error.connect(self.notify_error)

     
    def check_for_updates(self):
        self.update_checker_thread.start()


    # def download_and_install_update(self, download_url, latest_version):
    #     # self.main_window.close()

    #     # sleep(1000)
    #     try:
    #         # Download the update file
    #         response = requests.get(download_url, stream=True)
    #         if response.status_code == 200:
    #             update_file_path = os.path.join(tempfile.gettempdir(), f"update_{latest_version}.exe")
    #             with open(update_file_path, 'wb') as f:
    #                 for chunk in response.iter_content(chunk_size=8192):
    #                     f.write(chunk)
                
    #             self.update_downloaded.emit(update_file_path)

    #             # Overwrite the current executable with the downloaded file
    #             # current_executable = sys.argv[0]
    #             # os.rename(current_executable, current_executable + ".old")  # Backup current executable
    #             # os.rename(update_file_path, current_executable)

    #             # Restart the application
    #             subprocess.Popen([update_file_path])
                
    #             # Close the current application
    #             # QApplication.quit()
    #         else:
    #             self.update_error.emit(f"Failed to download update: {response.status_code}")
    #     except Exception as e:
    #         self.update_error.emit(str(e))


    def notify_update_found(self, latest_version_info):
        latest_version = latest_version_info['version']
        release_notes = latest_version_info.get('release_notes', 'No release notes available.')

        title = self.tr('Update Available')
        content = self.tr('A new version')+f" {latest_version} " + self.tr('is available. Do you want to download this version? \n\n') + self.tr('Release notes:\n') + f"{release_notes}"
        
        
        w = MessageBox(title, content, self.main_window)
        w.hideCancelButton()

        # w.setContentCopyable(True)
        if w.exec():
            download_url = latest_version_info['download_url']

            self.start_download(download_url)

            # self.download_and_install_update(download_url, latest_version)
        else:
            self.update_checker_thread.quit()
            self.update_checker_thread.wait()
            logger.info('Cancel button is pressed')

    def notify_no_update_found(self):
        if not self.start_up:
            title = self.tr('No Update')
            content = self.tr("You are using the latest version ") + f"{VERSION}."
            w = MessageBox(title, content, self.main_window)
            w.hideCancelButton()
            if w.exec():
                logger.info('Yes button is pressed')
        else:
            logger.info("Self-check when the program starts, no pop-up window required")

    def notify_error(self, error_message):
        title = self.tr('Error')
        content = self.tr(error_message,)
        w = MessageBox(title, content, self.main_window)
        w.hideCancelButton()
        if w.exec():
            logger.info('Yes button is pressed')

    def on_install_update(self, update_file_path):
        # import time
        # time.sleep(2)
        self.progress_window.close()

        title = self.tr('Update')
        content = self.tr("Ready to start installing the program. The program will be closed and restarted during the installation process. Please save your data.")
        w = MessageBox(title, content, self.main_window)
        w.hideCancelButton()
        if w.exec():
            
            try:
                command = [update_file_path]
                process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
                # process = subprocess.Popen(command)
                logger.info(f'Run {command}, return: {process.pid}')
            except subprocess.CalledProcessError as e:
                logger.error(f'Command failed with exit status {e.returncode}')
                logger.error(f'Stdout: {e.stdout}')
                logger.error(f'Stderr: {e.stderr}')
            except FileNotFoundError as e:
                logger.error(f'Command not found: {e}')
            except subprocess.TimeoutExpired as e:
                logger.error(f'Command timed out: {e}')
            except Exception as e:
                logger.error(f'An unexpected error occurred: {e}')

            QApplication.quit()   

    def start_download(self,download_url):
        self.progress_window = ProgressWindow(self.main_window)
        self.download_thread = DownloadThread(download_url,output_dir='', parent=self)
        self.download_thread.download_progress.connect(self.progress_window.set_progress)
        self.download_thread.download_complete.connect(self.on_install_update)
        self.download_thread.start()

        self.progress_window.show()
    
class ProgressWindow(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.titleLabel = SubtitleLabel(self.tr('Downloading'), self)

        # self.progress_bar = ProgressBar(self)
        self.progress_bar = ProgressRing(self)
        self.progress_bar.setFixedSize(100, 100)
        self.progress_bar.setTextVisible(True)

                # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.progress_bar)

        self.viewLayout.setAlignment(self.progress_bar, Qt.AlignCenter)
        self.widget.setMinimumWidth(360)
        self.widget.setMinimumHeight(160)
        self.hideYesButton()
        self.hideCancelButton()

    def set_progress(self, percent):
        self.progress_bar.setValue(percent)

    def reset_progress(self):
        self.progress_bar.setValue(0)
        self.hide()        