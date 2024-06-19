# 获取当前脚本的目录
$ScriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# 定义快捷方式的路径和目标文件路径
$ShortcutPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'FaceFusion.lnk')
$TargetPath = [System.IO.Path]::Combine($ScriptDirectory, 'run_facefusion.bat')
$IconPath = [System.IO.Path]::Combine($ScriptDirectory, 'facefusion.ico')

# 创建一个Shell对象
$WScriptShell = New-Object -ComObject WScript.Shell

# 创建快捷方式对象
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)

# 设置快捷方式的目标路径
$Shortcut.TargetPath = $TargetPath

# 可选：设置快捷方式的起始目录
$Shortcut.WorkingDirectory = $ScriptDirectory

# 可选：设置快捷方式的描述
# $Shortcut.Description = '指向example.txt的快捷方式'

# 可选：设置快捷方式的图标
$Shortcut.IconLocation = "$IconPath, 0"

# 保存快捷方式
$Shortcut.Save()

Write-Output "Creat shortcut：$ShortcutPath"
