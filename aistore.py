'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-16 04:58:48
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-20 13:54:19
FilePath: \aistore\demo.py
Description: main
'''
# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.view.main_window import MainWindow

from app.core.update import UpdateManager

# enable dpi scale
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)


# create main window
w = MainWindow()
w.show()

on_update = cfg.get(cfg.checkUpdateAtStartUp)
if on_update:
    update_manager = UpdateManager(w)
    update_manager.check_for_updates()
    
# app.exec_()
sys.exit(app.exec_())