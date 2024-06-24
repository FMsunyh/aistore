from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('app.installer.facefusion')
hiddenimports = collect_submodules('app.installer.kohya_ss')
hiddenimports = collect_submodules('app.installer.sd_webui')
