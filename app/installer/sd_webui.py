'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-19 15:21:55
FilePath: \aistore\app\installer\sd_webui.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from app.core.filesystem import is_file, is_image, is_video, resolve_relative_path
from app.core.download import is_download_done
from app.core import  process_manager
import app.core.globals
import winshell
import platform
import os
import sys

def pre_check() -> bool:
	# download_directory_path = resolve_relative_path('../.assets/models')
	# # model_url = get_options('model').get('url')
	# # model_path = get_options('model').get('path')

	# if not app.core.globals.skip_download:
	# 	process_manager.check()
	# 	conditional_download(download_directory_path, [ model_url ])
	# 	process_manager.end()
	# return is_file(model_path)
    print("Hello World, sd webui")
    
def process():
	print("Start install process")
    # _create_shortcut()
    
def _create_shortcut():
	if platform.system().lower() == 'windows':
		link_filepath = os.path.join(winshell.desktop(), "aistore.lnk")
		with winshell.shortcut(link_filepath) as link:
			link.path = r"D:\aistore\tmp\unpacked\aideskv2\bin\aidesk.exe"
			link.description = "Shortcut to python"
			# link.arguments = "-m winshell"
			link.icon_location=(r"D:/aistore/tmp/unpacked/aideskv2/bin/facefusion.ico", 0)
			link.working_directory = r"D:/aistore/tmp/unpacked/aideskv2/bin/"
	else:
		print("Linux is not support")