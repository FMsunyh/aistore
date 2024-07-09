'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-05 16:27:37
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-08 17:55:05
Description: download thread

'''
import subprocess
import sys
import os
import tempfile
import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from tqdm import tqdm

from app.core.filesystem import get_file_size, is_file

from app.common.logger import logger
import urllib.request
from functools import lru_cache

# import ptvsd

class DownloadThread(QThread):
    download_progress = pyqtSignal(int)
    download_complete = pyqtSignal(str)

    def __init__(self, url, output_dir='', parent=None):
        super().__init__(parent)
        self.url = url
        self.output_dir = output_dir

    def run(self):
        self._download_file()

    def _download_file(self):
        # ptvsd.debug_this_thread()
        filename = os.path.basename(self.url)

        if self.output_dir=='':
            ouput_path = os.path.join(tempfile.gettempdir(), filename)
        else:
            ouput_path = os.path.join(self.output_dir, filename)

        initial_size = get_file_size(ouput_path)
        total_size = self._get_download_size(self.url)
        if initial_size < total_size:
            try:
                command = [ 'curl', '--create-dirs', '--silent', '--insecure', '--location', '--continue-at', '-', '--output', ouput_path, self.url ]
                process = subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)
                # process = subprocess.Popen(command)
                logger.info(f'Run {command}, return: {process.pid}')
                current_size = initial_size
                while current_size < total_size:
                    if is_file(ouput_path):
                        current_size = get_file_size(ouput_path)
                        self.download_progress.emit(int((current_size / total_size) * 100))

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
                
        if total_size and not self._is_download_done(self.url, ouput_path):
            try:
                os.remove(ouput_path)
            except Exception as e:
                logger.error(f'An unexpected error occurred: {e}')
            self._download_file()

        self.download_progress.emit(100)
        self.download_complete.emit(ouput_path)

    @lru_cache(maxsize = None)
    def _get_download_size(self, url : str) -> int:
        try:
            response = urllib.request.urlopen(url, timeout = 10)
            return int(response.getheader('Content-Length'))
        except (OSError, ValueError):
            return 0

    def _is_download_done(self, url : str, file_path : str) -> bool:
        if is_file(file_path):
            return self._get_download_size(url) == get_file_size(file_path)
        return False