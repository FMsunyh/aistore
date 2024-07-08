chcp 65001
@echo off
set "PATH=%CD%\envs\;%CD%\envs\Library\mingw-w64\bin;%CD%\envs\Library\usr\bin;%CD%\envs\Library\bin;%CD%\envs\Scripts;%CD%\envs\bin;%CD%;%PATH%";
python webui.py --allow-code --medvram --xformers --enable-insecure-extension-access --api