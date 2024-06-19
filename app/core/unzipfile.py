
import zipfile


def extract_file(target_dir, target_zipfile):
	# target_dir = os.path.join('./tmp', 'unpacked')
	# target_zipfile = os.path.join('./tmp', 'aideskv2.zip')

	assert zipfile.is_zipfile(target_zipfile), 'The given file %s is corrupted!' %(target_zipfile)

	try:
		with zipfile.ZipFile(target_zipfile, 'r') as zip_ref:
			zip_ref.extractall(target_dir, members=None,)
	except zipfile.BadZipFile:
		print('Not a zip file or a corrupted zip file')