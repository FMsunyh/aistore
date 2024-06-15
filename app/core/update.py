import sys
import requests
import os
import subprocess
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMessageBox

CURRENT_VERSION = "1.0.0"
UPDATE_INFO_URL = "http://172.30.9.84/chfs/shared/latest_version_info.txt"  # Replace with your URL

class UpdateChecker(QThread):
    update_found = pyqtSignal(dict)
    no_update_found = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def run(self):
        try:
            response = requests.get(UPDATE_INFO_URL)
            print(response)
            if response.status_code == 200:
                latest_version_info = response.json()
                latest_version = latest_version_info['version']
                if latest_version != CURRENT_VERSION:
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
    update_downloaded = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.update_checker = UpdateChecker()
        self.update_checker.update_found.connect(self.update_available.emit)
        self.update_checker.no_update_found.connect(self.no_update_available.emit)
        self.update_checker.error_occurred.connect(self.update_error.emit)

        # Connect update manager signals to appropriate slots
        self.update_available.connect(self.notify_update_found)
        self.no_update_available.connect(self.notify_no_update_found)
        self.update_error.connect(self.notify_error)
        self.update_downloaded.connect(self.on_update_downloaded)

    def check_for_updates(self):
        self.update_checker.start()

    def download_and_install_update(self, download_url, latest_version):
        try:
            # Download the update file
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                update_file_path = os.path.join(os.getcwd(), f"update_{latest_version}.exe")
                with open(update_file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                self.update_downloaded.emit(update_file_path)

                # Overwrite the current executable with the downloaded file
                current_executable = sys.argv[0]
                os.rename(current_executable, current_executable + ".old")  # Backup current executable
                os.rename(update_file_path, current_executable)

                # Restart the application
                subprocess.Popen([current_executable])
                
                # Close the current application
                QApplication.quit()
            else:
                self.update_error.emit(f"Failed to download update: {response.status_code}")
        except Exception as e:
            self.update_error.emit(str(e))


    def notify_update_found(self, latest_version_info):
        latest_version = latest_version_info['version']
        release_notes = latest_version_info.get('release_notes', 'No release notes available.')
        reply = QMessageBox.question(
            None, 'Update Available',
            f"A new version ({latest_version}) is available.\n\nRelease Notes:\n{release_notes}\n\nDo you want to update?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            download_url = latest_version_info['download_url']
            self.download_and_install_update(download_url, latest_version)

    def notify_no_update_found(self):
        QMessageBox.information(None, 'No Update', 'You are using the latest version.')

    def notify_error(self, error_message):
        QMessageBox.critical(None, 'Error', error_message)

    def on_update_downloaded(self, update_file_path):
        QMessageBox.information(None, 'Update', f"Downloaded and installed update from {update_file_path}. The application will now restart.")