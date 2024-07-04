'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-24 14:14:17
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-04 17:54:56
FilePath: \aistore\app\core\install_worker.py
Description: uninstall worker
'''

import datetime
import os
import shutil
import subprocess
import ssl
import urllib.request
from typing import List
from functools import lru_cache

from app.core.registry import write_install_info_to_registry,delete_software_registry_info
from app.core.common_helper import is_macos
from app.core.filesystem import get_file_size, is_file
from PyQt5.QtCore import QThread, pyqtSignal, QObject

import os.path
# import ptvsd
from app.common.logger import logger

class UninstallWorker(QThread):
    progress = pyqtSignal(str, int)
    completed = pyqtSignal()

    def __init__(self, app_name:str, uninstall_directory:str, parent=None):
        super().__init__(parent)
        self.app_name = app_name
        self.uninstall_directory = os.path.join(uninstall_directory, self.app_name)

    def run(self):
        # ptvsd.debug_this_thread()
        logger.info(f"Start to uninstall {self.app_name}")
		
        self._delete_files()

        reg_path = os.path.join(r"Software\aistore", self.app_name)
        delete_software_registry_info(reg_path)
        
        self.completed.emit()
        logger.info(f"Finished")

    def _delete_files(self):
        logger.info(f"Start to delete files {self.app_name}")

        total_files = sum([len(files) for r, d, files in os.walk(self.uninstall_directory)])
        deleted_files = 0

        for root, dirs, files in os.walk(self.uninstall_directory, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files += 1
                    self.progress.emit(f'remove {self.app_name}' ,int((deleted_files / total_files) * 100))
                except Exception as e:
                    logger.error(f"Error deleting file {file_path}: {e}")
                    self.progress.emit(f'Error',  -1)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                except Exception as e:
                    logger.error(f"Error deleting directory {dir_path}: {e}")
                    self.progress.emit(f'Error',  -1)
        try:
            shutil.rmtree(self.uninstall_directory)
            self.completed.emit()
            logger.info(f"Finished")

        except Exception as e:
            logger.error(f"Error deleting root directory {self.uninstall_directory}: {e}")
            self.progress.emit(f'Error',  -1)