<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-06-14 18:28:18
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-07-26 11:34:58
 * @FilePath: \aistore\README.md
 * @Description: Content of readme
-->
# aistore
Build a aistore for cloud

Preview
-------
![Preview](Preview.PNG)

## Icon resource

Add new icon, you need to rebuild the resource file.
```bash
cd aistore
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```

## Build
Build executable file 
```
pyinstaller --onefile  .\aistore.py
```

```
pyinstaller --onefile  --noconsole  --icon=.\aistore.ico .\aistore.py
```

```
pyinstaller --onefile  --noconsole  --distpath .\.PyInstaller --icon=.\aistore.ico .\aistore.py
```

```
pyinstaller --onefile --additional-hooks-dir=.\app\installer .\aistore.py
```

OR
```
pyinstaller aistore.spec --distpath .\.PyInstaller
```

## 翻译
```sh
lupdate .\aistore.pro
```

```
linguist app/resource/i18n/gallery.zh_CN.ts
```


```
lrelease app/resource/i18n/gallery.zh_CN.ts
```

重新编译资源
```
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```

##  激活myenv
```
python -m venv myenv
myenv\Scripts\activate  # On Windows
source myenv/bin/activate  # On macOS/Linux
pip install pyinstaller

```


Documentation
-------------

需要下载QT的工具

- 5.14之前的版本，可以用离线安装

    下载  [qt5.14.2](https://download.qt.io/archive/qt/5.14/5.14.2/qt-opensource-windows-x86-5.14.2.exe)
    [Windows/Linux(命令、安装包和源码安装)平台各个版本QT详细安装教程](https://blog.csdn.net/new9232/article/details/132590691)


- 5.15后的版本，没有离线安装包了，都是在线安装包

    [Windows下安装QT，遇到下载组件中没有指定版本(提供解决方式) + 5.15详细安装步骤版](https://blog.csdn.net/qq_38141255/article/details/136968221)

创建桌面快捷方式
[python Shortcuts](https://winshell.readthedocs.io/en/latest/shortcuts.html)


[解决Python+vscode环境，QThread 线程无法加入断点问题](https://blog.csdn.net/kanbang/article/details/133808155)

[PowerShell：因为在此系统上禁止运行脚本，解决方法](https://syxdevcode.github.io/2021/09/04/PowerShell%EF%BC%9A%E5%9B%A0%E4%B8%BA%E5%9C%A8%E6%AD%A4%E7%B3%BB%E7%BB%9F%E4%B8%8A%E7%A6%81%E6%AD%A2%E8%BF%90%E8%A1%8C%E8%84%9A%E6%9C%AC%EF%BC%8C%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)


[PyQt5 pyqtSignal: 自定义信号传入的参数方法](https://blog.csdn.net/qq_39560620/article/details/105711799)


[button.clicked.connect(lambda checked, i=i: self.on_button_clicked(i))](https://stackoverflow.com/questions/35819538/using-lambda-expression-to-connect-slots-in-pyqt)

[超全的VSCode快捷键，收藏！](https://juejin.cn/post/7258140838139641917)

[chsf](https://github.com/ods-im/CuteHttpFileServer)