# aistore
Build a aistore for cloud

## Icon resource

Add new icon, you need to rebuild the resource file.

```bash
cp aistore
pyrcc5 -o ./app/common/resource.py ./app/resource/resource.qrc
```