'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-24 14:14:17
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-24 18:39:11
FilePath: \aistore\app\core\install_worker.py
Description: install worker
'''

import datetime
import os
import shutil
import subprocess
import ssl
import urllib.request
from typing import List
from functools import lru_cache
from tqdm import tqdm

import app.core.globals
from app.core.registry import write_install_info_to_registry,delete_software_registry_info
import app.core.wording
from app.core.common_helper import is_macos
from app.core.filesystem import get_file_size, is_file
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from app.common.config import cfg

import sys
import os.path
import zipfile
import ptvsd

class InstallWorker(QThread):
	# process_bar = pyqtSignal(int)  # 自定义信号用于任务完成后传递结果
	download_progress = pyqtSignal(str, int)
	download_completed = pyqtSignal(str)
	
	unzip_progress = pyqtSignal(str, int)  # 信号传递解压状态
	unzip_completed = pyqtSignal(str)  # 信号传递解压状态

	completed = pyqtSignal(str)  # 信号传递解压状态

	def __init__(self, name : str, version : str, download_directory_path : str, url : str, install_directory : str, parent=None):
		super().__init__(parent)

		self.name = name
		self.version = version
		self.download_directory_path = download_directory_path
		self.url = url

		self.filename = os.path.basename(self.url)
		self.download_file_path = os.path.join(self.download_directory_path, self.filename)

		self.install_directory = install_directory

	def run(self):
		ptvsd.debug_this_thread()
		self._download_file()
		output = self._extract_file(self.download_file_path, self.install_directory)
		self._create_shortcut(output)
		self._create_registy()
		
		self.completed.emit(self.name)

	def _download_file(self):
		ptvsd.debug_this_thread()

		log_level = 'error'
		initial_size = get_file_size(self.download_file_path)
		download_size = self._get_download_size(self.url)
		if initial_size < download_size:
			with tqdm(total = download_size, initial = initial_size, desc = app.core.wording.get('downloading'), unit = 'B', unit_scale = True, unit_divisor = 1024, ascii = ' =', disable = log_level in [ 'warn', 'error' ]) as progress:
				process = subprocess.Popen([ 'curl', '--create-dirs', '--silent', '--insecure', '--location', '--continue-at', '-', '--output', self.download_file_path, self.url ])
				# stdout, stderr = process.communicate()
				current_size = initial_size
				while current_size < download_size:
					if is_file(self.download_file_path):
						current_size = get_file_size(self.download_file_path)
						progress.update(current_size - progress.n)

						progress_percentage = int((current_size / download_size) * 50)
						self.download_progress.emit(self.filename, progress_percentage)

		if download_size and not self._is_download_done(self.url, self.download_file_path):
			os.remove(self.download_file_path)
			self.run(self.download_directory_path, self.url)

		self.download_progress.emit(self.filename, 50)
		self.download_completed.emit(self.filename)

	def _extract_file(self, zipfile_path, output):
		assert zipfile.is_zipfile(zipfile_path), 'The given file %s is corrupted!' %(zipfile_path)

		try:
			with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
				file_list = zip_ref.infolist()
				total_files = len(file_list)
				for i, file in enumerate(file_list):
					zip_ref.extract(file, output)
					progress_percentage = int((i + 1) / total_files * 100) + 50
					self.unzip_progress.emit(self.filename, progress_percentage)
					
			self.unzip_completed.emit(self.filename)

		except zipfile.BadZipFile:
			self.unzip_progress.emit(self.filename, -1)
			print('Not a zip file or a corrupted zip file')
		
		app_path = os.path.join(output, self.name)
		os.rename(os.path.join(output, f"{self.name}-{self.version}"), app_path)
		return app_path

	def _create_shortcut(self, target_path):

		# PowerShell脚本的路径
		ps_script_path = os.path.join(target_path,"createshortcut.ps1") 

		command = ["powershell.exe", "-Command"," Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"]
		result = subprocess.run(command, capture_output=True, text=True)

		# 构建PowerShell命令
		command = ["powershell.exe", "-File", ps_script_path]
		# 执行PowerShell命令
		result = subprocess.run(command, capture_output=True, text=True)

		command = ["powershell.exe", "-Command", "set-executionpolicy restricted -Scope CurrentUser -Force"]
		result = subprocess.run(command, capture_output=True, text=True)

		# 打印输出
		print(result.stdout)
		if result.stderr:
			print("Error:", result.stderr)
		

	def _create_registy(self):
		software_name, software_version = os.path.basename(self.url).split('-')

		reg_path = os.path.join(r"Software\aistore", software_name)
		software_publisher = "MyCompany"
		installation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_install_info_to_registry(reg_path,software_name, software_version[:-4], software_publisher, installation_date)

	
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