<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-07-01 10:56:29
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-07-26 16:33:15
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

4. 发布到线上
```sh
cd D:\aistore
python upload_installer.py

```


最终脚本:
```sh
cd D:\aistore
```

```sh
powershell -noexit -ExecutionPolicy Bypass -File .\release.ps1
```

服务器
```vim
aistore
ip：120.233.206.35
user：ads
pwd：unaigc2024
```

测试机
```
1697498519
asd123456
```

chfs
```
1 013 260 179
11111
```

转移数据
scp -r D:\ai_store\* ads@172.30.5.254:/mnt/ai_store