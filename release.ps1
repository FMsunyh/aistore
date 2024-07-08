# 发布步骤

# 1. 初始化数据
Write-Host "Step 1: Initializing data"
cd D:\aistore
python do_initializer_db.py

# 2. PyInstaller 翻译
Write-Host "Step 2: Running PyInstaller translations"
cd D:\aistore
# lupdate .\aistore.pro
# linguist app/resource/i18n/gallery.zh_CN.ts
# lrelease app/resource/i18n/gallery.zh_CN.ts

# 重新编译资源
Write-Host "Recompiling resources"
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc

Write-Host "Creating PyInstaller package"
pyinstaller --onefile --noconsole --distpath .\.pyInstaller --icon=.\aistore.ico .\aistore.py
# pyinstaller aistore.spec --distpath .\.PyInstaller

# 3. NSIS编译安装程序
Write-Host "Step 3: Compiling installer with NSIS"
cd D:\aistore\.install
makensis ./aistore.nsi


# 4. 发布到线上
Write-Host "Step 4: Upload the new version to http server"
cd D:\aistore
python upload_installer.py


cd D:\aistore
Write-Host "Publishing completed"
