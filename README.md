<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-06-14 18:28:18
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-06-19 11:40:16
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