# aistore
Build a aistore for cloud

## Icon resource

Add new icon, you need to rebuild the resource file.

```bash
cp aistore
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```

```
pyinstaller --onefile  .\demo.py
```

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
