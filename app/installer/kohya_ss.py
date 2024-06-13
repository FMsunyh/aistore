
from app.core.filesystem import is_file, is_image, is_video, resolve_relative_path
from app.core.download import conditional_download, is_download_done
from app.core import  process_manager
import app.core.globals

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