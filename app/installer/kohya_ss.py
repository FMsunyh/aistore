
from app.core.filesystem import is_file, is_image, is_video, resolve_relative_path
from app.core.download import conditional_download, is_download_done,unzipfile
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
    print("Hello World, kohya_ss GUI")
    unzipfile()
    _create_shortcut()
    
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