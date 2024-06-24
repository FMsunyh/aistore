'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-24 10:57:55
FilePath: \aistore\app\installer\facefusion.py
Description: Installer of facefusion
'''

from pathlib import Path
import tempfile
from app.core.filesystem import create_temp, is_file, is_image, is_video, resolve_relative_path
from app.core.download import is_download_done,get_download_manager
from app.core import  process_manager
import app.core.globals
import winshell
import platform
import os
import sys

from app.core.unzipfile import extract_file
from app.common.config import SERVER_IP,SERVER_PORT

def pre_check() -> bool:

	# download_directory_path = resolve_relative_path('../.assets/models')
	# # model_url = get_options('model').get('url')
	# # model_path = get_options('model').get('path')

	# if not app.core.globals.skip_download:
	# 	process_manager.check()
	# 	conditional_download(download_directory_path, [ model_url ])
	# 	process_manager.end()
	# return is_file(model_path)
    print("Hello World, FaceFusion")

def process(ring_value_changedSig, finished):
	app_url = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/facefusion/facefusion-2.6.0.zip"
	print("Start install process")
	temp_directory_path = os.path.join(tempfile.gettempdir(), 'aistore', 'facefusion')
	Path(temp_directory_path).mkdir(parents = True, exist_ok = True)
	print(temp_directory_path)

	get_download_manager().start_task(temp_directory_path, app_url,ring_value_changedSig,finished)

	download_file_path = os.path.join(temp_directory_path, os.path.basename(app_url))
	
	# app_path = "D:\myapp"
	# extract_file(download_file_path, app_path)

	# _create_shortcut(os.path.join(app_path, 'facefusion'))

	# finished.emit()

# def _create_shortcut(app_path):
# 	if platform.system().lower() == 'windows':
# 		link_filepath = os.path.join(winshell.desktop(), "facefusion.lnk")
# 		with winshell.shortcut(link_filepath) as link:
# 			link.path = os.path.join(app_path, "run_facefusion.bat")
# 			link.description = "Shortcut to facefusion"
# 			# link.arguments = "-m winshell"
# 			link.icon_location=(os.path.join(app_path,"facefusion.ico"), 0)
# 			link.working_directory = app_path
# 	else:
# 		print("Linux is not support")

def install(app_card):
	print("Start install process (facefusion)")

	app_url = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/facefusion/facefusion-2.6.0.zip"
	temp_directory_path = os.path.join(tempfile.gettempdir(), 'aistore', 'facefusion')
	Path(temp_directory_path).mkdir(parents = True, exist_ok = True)
	print(temp_directory_path)

	get_download_manager().install_task(temp_directory_path, app_url, app_card)

def uninstall(registy_info):
	get_download_manager().uninstall_task(registy_info)
	# for item in registy:
	# 	print(item)

	print("uninstall facefusion") 