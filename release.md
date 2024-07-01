<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-07-01 10:56:29
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-07-01 11:52:33
 * @FilePath: \aistore\Release.md
 * @Description: 发布版本
-->
# 发布步骤

1. 初始化数据

```sh
cd D:\aistore
python do_initializer_db.py
```

2. Pyinstaller
翻译

```sh
cd D:\aistore
```

```sh
lupdate .\aistore.pro
```
```sh
linguist app/resource/i18n/gallery.zh_CN.ts
```
```sh
lrelease app/resource/i18n/gallery.zh_CN.ts
```

重新编译资源
```sh
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```

```sh
pyinstaller --onefile  --noconsole  --distpath .\.pyInstaller --icon=.\aistore.ico .\aistore.py
```

```sh
pyinstaller aistore.spec --distpath .\.PyInstaller
```

3. NSIS编译安装程序
```sh
cd D:\aistore\.install
```

```sh
makensis ./aistore.nsi
```

最终脚本:
```sh
cd D:\aistore
```

```sh
powershell -noexit -ExecutionPolicy Bypass -File .\release.ps1
```