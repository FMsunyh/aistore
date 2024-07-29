'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-14 18:28:18
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-29 11:56:55
FilePath: \aistore\app\common\config.py
Description: config for aistore
'''
# coding:utf-8
from pathlib import Path
import sys
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer)

from app.common.config_ip import CONFIG_IP
from version import __author__, __version__
class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    # folders
    musicFolders = ConfigItem(
        "Folders", "LocalMusic", [], FolderListValidator())
    downloadFolder = ConfigItem(
        "Folders", "Download", "app/download", FolderValidator())
    
    cacheFolder = ConfigItem(
        "Folders", "CacheFolder", "app/cache", FolderValidator(), restart=True)
    
    install_folder = ConfigItem(
    "Folders", "Intall", "D:/aistore", FolderValidator())
    

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.CHINESE_SIMPLIFIED, OptionsValidator(Language), LanguageSerializer(), restart=True)

    # Material
    blurRadius  = RangeConfigItem("Material", "AcrylicBlurRadius", 15, RangeValidator(0, 40))

    # software update
    checkUpdateAtStartUp = ConfigItem("Update", "CheckUpdateAtStartUp", True, BoolValidator())


YEAR = 2024
AUTHOR = __author__
VERSION = __version__
APP_NAME = 'AIStore'
HELP_URL = "https://www.zjusmart.com/#/"
REPO_URL = "https://manage.zjusmart.com/vmt/web/user/login"
EXAMPLE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/master/examples"
FEEDBACK_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues"
RELEASE_URL = "https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases/latest"
ZH_SUPPORT_URL = "https://qfluentwidgets.com/zh/price/"
EN_SUPPORT_URL = "https://qfluentwidgets.com/price/"

REGISTY_PATH = r"Software\aistore"

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('app/config/config.json', cfg)


GeoLite2_database = str("app/cache/GeoLite2-City.mmdb")
SERVER_IP = CONFIG_IP(GeoLite2_database)

# SERVER_IP = "183.232.235.52"
# SERVER_IP = "172.30.9.84" # local test
SERVER_PORT = "7860"

UPDATE_INFO_URL = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/latest_version_info.json"  # Replace with your URL