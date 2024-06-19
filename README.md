<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-06-14 18:28:18
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-06-19 17:18:54
 * @FilePath: \aistore\README.md
 * @Description: Content of readme
-->
# aistore
Build a aistore for cloud

## Icon resource

Add new icon, you need to rebuild the resource file.
```bash
cd aistore
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```

## Build
Build executable file 
```
pyinstaller --onefile  .\demo.py
```

OR
```
pyinstaller demo.spec
```

激活myenv
```
python -m venv myenv
myenv\Scripts\activate  # On Windows
source myenv/bin/activate  # On macOS/Linux
pip install pyinstaller

```

创建桌面快捷方式
[python Shortcuts](https://winshell.readthedocs.io/en/latest/shortcuts.html)


[解决Python+vscode环境，QThread 线程无法加入断点问题](https://blog.csdn.net/kanbang/article/details/133808155)

[PowerShell：因为在此系统上禁止运行脚本，解决方法](https://syxdevcode.github.io/2021/09/04/PowerShell%EF%BC%9A%E5%9B%A0%E4%B8%BA%E5%9C%A8%E6%AD%A4%E7%B3%BB%E7%BB%9F%E4%B8%8A%E7%A6%81%E6%AD%A2%E8%BF%90%E8%A1%8C%E8%84%9A%E6%9C%AC%EF%BC%8C%E8%A7%A3%E5%86%B3%E6%96%B9%E6%B3%95/)