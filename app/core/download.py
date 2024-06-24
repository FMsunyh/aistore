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

import sys
import os.path
import zipfile
import ptvsd

DOWNLOADMANAGER = None

def get_download_manager():
	global DOWNLOADMANAGER
	if DOWNLOADMANAGER == None:
		DOWNLOADMANAGER = DownloadManager()
	return DOWNLOADMANAGER

if is_macos():
	ssl._create_default_https_context = ssl._create_unverified_context

class DownloadWorker(QThread):
	# process_bar = pyqtSignal(int)  # 自定义信号用于任务完成后传递结果

	def __init__(self, download_directory_path : str, url : str, app_card, parent=None):
		super().__init__(parent)
		self.download_directory_path = download_directory_path
		self.url = url
		self.app_card = app_card

	def run(self):
		# ptvsd.debug_this_thread()
		zipfile_path = self.download_file()
		output = self.extract_file(zipfile_path, r"D:/aistore app/")
		# path = os.path.join(r"D:/aistore app/", self.app_card.name)
		self.create_shortcut(output)
		self.create_registy()

	# def run(self):
	# 	# 在子线程中运行长时间任务
	# 	process = subprocess.Popen([self.command, self.args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# 	stdout, stderr = process.communicate()
	# 	self.finished.emit(stdout.decode(), stderr.decode()) # 任务完成后发射信号
		
	def download_file(self):
		ptvsd.debug_this_thread()
		log_level = 'error'
		download_file_path = os.path.join(self.download_directory_path, os.path.basename(self.url))
		initial_size = get_file_size(download_file_path)
		download_size = get_download_size(self.url)
		if initial_size < download_size:
			with tqdm(total = download_size, initial = initial_size, desc = app.core.wording.get('downloading'), unit = 'B', unit_scale = True, unit_divisor = 1024, ascii = ' =', disable = log_level in [ 'warn', 'error' ]) as progress:
				process = subprocess.Popen([ 'curl', '--create-dirs', '--silent', '--insecure', '--location', '--continue-at', '-', '--output', download_file_path, self.url ])
				# stdout, stderr = process.communicate()
				current_size = initial_size
				current_bar = 0
				while current_size < download_size:
					if is_file(download_file_path):
						current_size = get_file_size(download_file_path)
						progress.update(current_size - progress.n)
						progress_percentage = int((current_size / download_size) * 50)
						if current_bar < progress_percentage:
							current_bar = progress_percentage
							# self.process_bar.emit(progress_percentage) # 任务完成后发射信号
							self.app_card.ring_value_changedSig.emit(progress_percentage)


		if download_size and not is_download_done(self.url, download_file_path):
			os.remove(download_file_path)
			self.run(self.download_directory_path, self.url, self.app_card)

		return download_file_path
	
	def extract_file(self, zipfile_path, output):
		assert zipfile.is_zipfile(zipfile_path), 'The given file %s is corrupted!' %(zipfile_path)

		try:
			# with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
			# 	zip_ref.extractall(output, members=None,)

			with zipfile.ZipFile(zipfile_path, 'r') as zip_ref:
				file_list = zip_ref.infolist()
				total_files = len(file_list)
				for i, file in enumerate(file_list):
					zip_ref.extract(file, output)
					progress_percentage = int((i + 1) / total_files * 100) + 50
					self.app_card.ring_value_changedSig.emit(progress_percentage)
					
					# print(zip_ref.filename)
		except zipfile.BadZipFile:
			print('Not a zip file or a corrupted zip file')
		
		name_version = os.path.basename(zipfile_path)[:-4]
		app_path = os.path.join(output, self.app_card.name)
		os.rename(os.path.join(output, name_version), app_path)
		return app_path

	def create_shortcut(self, target_path):

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
		

	def create_registy(self):
		software_name, software_version = os.path.basename(self.url).split('-')

		reg_path = os.path.join(r"Software\aistore", software_name)
		software_publisher = "MyCompany"
		installation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		write_install_info_to_registry(reg_path,software_name, software_version[:-4], software_publisher, installation_date)

class UninstallWorker(QThread):
	process_bar = pyqtSignal(int)  # 自定义信号用于任务完成后传递结果

	def __init__(self, app_name, parent=None):
		super().__init__(parent)
		self.app_name = app_name


	def run(self):
		# ptvsd.debug_this_thread()
		# zipfile_path = self.download_file()
		# output = self.extract_file(zipfile_path, "D:\myapp")
		directory_path = os.path.join(r"D:/aistore app",self.app_name )
		if os.path.exists(directory_path):
			print("delete directory {}".format(directory_path))
			# os.rmdir(directory_path)
			shutil.rmtree(directory_path)
			# os.removedirs(directory_path)
		
		software_name = self.app_name
		reg_path = os.path.join(r"Software\aistore", software_name)
		delete_software_registry_info(reg_path)

class DownloadManager(QObject):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.worker = None
		self.uninstall_worker = None
		self.ring_value_changedSig = None
		self.install_finishedSig = None

	def start_task(self, download_directory_path, urls, ring_value_changedSig, finished):
		# self.finished = finished
		# self.worker = DownloadWorker(download_directory_path, urls, ring_value_changedSig)
		# self.worker.process_bar.connect(self.on_process_bar)
		# self.worker.finished.connect(self.finished.emit)
		# self.worker.start()
		pass

	def install_task(self, download_directory_path, urls, app_card):
		self.install_finishedSig = app_card.install_finishedSig
		self.worker = DownloadWorker(download_directory_path, urls, app_card)
		# self.worker.process_bar.connect(self.on_process_bar)
		self.worker.finished.connect(self.install_finishedSig.emit)
		self.worker.start()

		# self.worker.wait()

	def uninstall_task(self, app_name):
		self.uninstall_worker = UninstallWorker(app_name=app_name)
		self.uninstall_worker.start()


	# def on_process_bar(self, current_size):
	# 	self.worker.ring_value_changedSig.emit(current_size)

	def wait(self):
		self.worker.wait()

# def conditional_download(download_directory_path : str, urls : List[str]) -> None:
# 	log_level = 'error'
# 	for url in urls:
# 		download_file_path = os.path.join(download_directory_path, os.path.basename(url))
# 		initial_size = get_file_size(download_file_path)
# 		download_size = get_download_size(url)
# 		if initial_size < download_size:
# 			with tqdm(total = download_size, initial = initial_size, desc = app.core.wording.get('downloading'), unit = 'B', unit_scale = True, unit_divisor = 1024, ascii = ' =', disable = log_level in [ 'warn', 'error' ]) as progress:
# 				subprocess.Popen([ 'curl', '--create-dirs', '--silent', '--insecure', '--location', '--continue-at', '-', '--output', download_file_path, url ])
# 				current_size = initial_size
# 				while current_size < download_size:
# 					if is_file(download_file_path):
# 						current_size = get_file_size(download_file_path)
# 						progress.update(current_size - progress.n)
# 		if download_size and not is_download_done(url, download_file_path):
# 			os.remove(download_file_path)
# 			conditional_download(download_directory_path, [ url ])


@lru_cache(maxsize = None)
def get_download_size(url : str) -> int:
	try:
		response = urllib.request.urlopen(url, timeout = 10)
		return int(response.getheader('Content-Length'))
	except (OSError, ValueError):
		return 0


def is_download_done(url : str, file_path : str) -> bool:
	if is_file(file_path):
		return get_download_size(url) == get_file_size(file_path)
	return False


# def unzipfile():
# 	target_dir = os.path.join('./tmp', 'unpacked')
# 	target_zipfile = os.path.join('./tmp', 'aideskv2.zip')

# 	assert zipfile.is_zipfile(target_zipfile), 'The given file %s is corrupted!' %(target_zipfile)

# 	try:
# 		with zipfile.ZipFile(target_zipfile, 'r') as zip_ref:
# 			zip_ref.extractall(target_dir, members=None,)
# 	except zipfile.BadZipFile:
# 		print('Not a zip file or a corrupted zip file')

	# Output:
	# 'Not a zip file or a corrupted zip file'

