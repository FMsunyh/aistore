import json
import sys
sys.path.insert(0, r'D:/aistore')
import requests
import argparse
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication

import os
from version import __author__,__version__

from app.common.config import SERVER_IP, SERVER_PORT
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
                self.delete_finished.emit(True, "File deleteed successfully!")
            else:
                self.delete_finished.emit(False, f"Failed to delete file. Status code: {response.status_code}")
        except Exception as e:
            self.delete_finished.emit(False, f"Exception occurred: {str(e)}")

    def _upload_file(self):
        # ptvsd.debug_this_thread()
        try:
            filename = os.path.basename(self.file_path)
            print(filename)
            with open(self.file_path, 'rb') as file:
                data = file.read()

            payload = {
                'folder': os.path.join(self.folder),
                'file': (filename, data)
            }

            response = requests.post(f"{self.url}/upload", files=payload)

            if response.status_code == 201:
                self.upload_finished.emit(True, "File uploaded successfully!")
            else:
                self.upload_finished.emit(False, f"Failed to upload file. Status code: {response.status_code}")
        except Exception as e:
            self.upload_finished.emit(False, f"Exception occurred: {str(e)}")
       

def rewrite_version(version_info_path):
    with open(version_info_path, 'r') as file:
        data = json.load(file)
        data['version'] = __version__
        data['download_url'] = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/AIStoreInstaller_{__version__}.exe"

    with open(version_info_path, 'w') as file:
        json.dump(data, file, indent=4)


def on_delete_finished(success, message):
    if success:
        print("Success:", message)
    else:
        print("Error:", message)
    

def on_upload_finished(success, message):
    if success:
        print("Success:", message)
    else:
        print("Error:", message)
    QCoreApplication.quit()

def main(file_path, url, folder):
    upload_thread = FileUploaderThread(file_path, url, folder)
    upload_thread.delete_finished.connect(on_delete_finished)
    upload_thread.upload_finished.connect(on_upload_finished)
    upload_thread.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a file to a specified URL.')
    # parser.add_argument('file_path', type=str, help='The path to the file to upload.')
    # parser.add_argument('version_info_path', type=str, help='The path to the file to upload.')
    # args = parser.parse_args()

    app = QCoreApplication(sys.argv)

    url = f'http://{SERVER_IP}:{SERVER_PORT}/chfs'
    file_path = f'.install\AIStoreInstaller_{__version__}.exe'
    version_info_path = f'.install\latest_version_info.json'

    rewrite_version(version_info_path)

    main(file_path, url,'/aistore_installer')
    main(version_info_path, url,'/')

    sys.exit(app.exec_())
