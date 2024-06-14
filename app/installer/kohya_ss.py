
from app.core.filesystem import is_file, is_image, is_video, resolve_relative_path
from app.core.download import conditional_download, is_download_done,unzipfile
from app.core import  process_manager
import app.core.globals
import winshell
import platform
import os


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
    _create_shortcut()
    
def _create_shortcut():
	if platform.system().lower() == 'windows':
		desktop_path = winshell.desktop()
		shortcut = winshell.shortcut()
		shortcut.path="/home/syh/workspace/aistore/tmp" # 设置谈捷方式的目标路径
			
		shortcut.write(os.path.join( desktop_path+"shortcut.lnk")) # 将诀捷方式保存劉泉面
		shortcut.icon_location="/home/syh/workspace/aistore/tmp/unpacked/aideskv2/bin/facefusion.ico" # 设置快捷方式的留标路径
		shortcut.target_path="/home/syh/workspace/aistore/tmp/unpacked/aideskv2/bin/aidesk.exe" # 设置块捷方式的目标路径
		# shortcut.arguments="-arg1 value1 -arg2 value2"

		shortcut.description="My Shortcut" 
		shortcut.save() 
	else:
		print("Linux is not support")