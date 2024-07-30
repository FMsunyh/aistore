import json
import sys
sys.path.insert(0, r'D:/aistore')
import requests
import argparse
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication

import os
from version import __author__,__version__

from app.common.config import SERVER_IP, SERVER_PORT
from app.common.logger import logger
# import ptvsd

class FileUploaderThread(QThread):
    upload_finished = pyqtSignal(bool, str)
    delete_finished = pyqtSignal(bool, str)

    def __init__(self, file_path, url, folder):
        super().__init__()
        self.file_path = file_path
        self.url = url
        self.folder = folder

    def run(self):
        # ptvsd.debug_this_thread()
        self._delete_file()
        self._upload_file()

    def _delete_file(self):
        # ptvsd.debug_this_thread()

        filename = os.path.basename(self.file_path)
        payload = {
                'filepath': os.path.join(self.folder, filename)
            }
        try:
            response = requests.delete(f"{self.url}/rmfiles", params=payload)

            if response.status_code == 204:
                self.delete_finished.emit(True, f"File deleted successfully! {self.file_path}")
            else:
                self.delete_finished.emit(False, f"Failed to delete file {self.file_path}. Status code: {response.status_code}")
        except Exception as e:
            self.delete_finished.emit(False, f"Exception occurred: {str(e)}")

    def _upload_file(self):
        # ptvsd.debug_this_thread()
        try:
            filename = os.path.basename(self.file_path)
            # logger.info(filename)
            with open(self.file_path, 'rb') as file:
                data = file.read()

            payload = {
                'folder': os.path.join(self.folder),
                'file': (filename, data)
            }

            response = requests.post(f"{self.url}/upload", files=payload)

            if response.status_code == 201:
                self.upload_finished.emit(True, f"File uploaded successfully! {self.file_path}")
            else:
                self.upload_finished.emit(False, f"Failed to upload file. {self.file_path}. Status code: {response.status_code}")
        except Exception as e:
            self.upload_finished.emit(False, f"Exception occurred: {str(e)}")
       

def rewrite_version(version_info_path):
    with open(version_info_path, 'r') as file:
        data = json.load(file)
        data['version'] = __version__
        data['download_url'] = f"AIStoreInstaller_{__version__}.exe"
        # data['download_url'] = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/aistore_installer/AIStoreInstaller_{__version__}.exe"
        print(data['download_url'])
    with open(version_info_path, 'w') as file:
        json.dump(data, file, indent=4)

    logger.info(f"latest_version_info: {data['version']}")


def on_delete_finished(success, message):
    if success:
        logger.info(f"Success: {message}")
    else:
        logger.info(f"Error: {message}")
    

def on_upload_finished(success, message):
    if success:
        logger.info(f"Success: {message}")
    else:
        logger.info(f"Error: {message}")


def create_thread(file_path, url, folder):
    thread = FileUploaderThread(file_path, url, folder)
    thread.delete_finished.connect(on_delete_finished)
    thread.upload_finished.connect(on_upload_finished)
    return thread

if __name__ == '__main__':
    app = QCoreApplication(sys.argv)
    url = f'http://{SERVER_IP}:{SERVER_PORT}/chfs'
    # url = f'http://120.233.206.35:{SERVER_PORT}/chfs'
    # url = f'http://45.254.27.97:{SERVER_PORT}/chfs'

    print(url)
    file_path = f'.install/AIStoreInstaller_{__version__}.exe'
    version_info_path = f'.install/latest_version_info.json'

    rewrite_version(version_info_path)
    
    threads = []
    t1 = create_thread(file_path, url, '/aistore_installer')
    t2 = create_thread(version_info_path, url, '/')

    threads.append(t1)
    threads.append(t2)

    def check_threads():
        for t in threads:
            if t.isRunning():
                return False
        return True

    def quit_if_threads_finished():
        if check_threads():
            app.quit()

    for t in threads:
        t.finished.connect(quit_if_threads_finished)

    for t in threads:
        t.start()

    sys.exit(app.exec_())
