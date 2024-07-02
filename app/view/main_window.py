'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-16 05:28:37
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-01 16:57:08
FilePath: \aistore\app\view\main_window.py
Description: main windows
'''
# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from app.core.registry import read_all_installed_software_from_registry
from app.core.update import UpdateManager
from app.database.db_initializer import DBInitializer
from app.database.library import Library
from app.view.app_interface import AppInterface

from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .navigation_view_interface import NavigationViewInterface
from .setting_interface import SettingInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg, REGISTY_PATH,HELP_URL
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()
        self.createWidgets()

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.setCustomBackgroundColor(QColor(240, 244, 249), QColor(32, 32, 32))

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.initWidget()


        self.splashScreen.finish()

        self.init_data()
        # self.check_software_registy()

        self.onInitFinished()
    
    def createWidgets(self):
        DBInitializer.init()
        self.library = Library(QSqlDatabase.database(DBInitializer.CONNECTION_NAME))
    
        # create sub interface
        self.homeInterface = HomeInterface(library = self.library, parent=self)
        self.navigationViewInterface = NavigationViewInterface(self)
        self.settingInterface = SettingInterface(self)

        self.appInterface = AppInterface(icon=":/qfluentwidgets/images/logo.png", name='AIStore', title='AIStore', content='AIStore Software Manager is a tool provided by ZhongJu Cloud that integrates software downloading, updating, uninstalling and optimization.', parent=self)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))


        # self.addSubInterface(self.aistoreInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        
        # self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        # self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        # self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX,t.basicInput, pos)
        # self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, pos)
        # self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, pos)
        # self.addSubInterface(self.layoutInterface, FIF.LAYOUT, t.layout, pos)
        # self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        # self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        # self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        # self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        # self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        # self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        # self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)

        # # add custom widget to bottom
        # self.navigationInterface.addItem(
        #     routeKey='price',
        #     icon=Icon.PRICE,
        #     text=t.price,
        #     onClick=self.onSupport,
        #     selectable=False,
        #     tooltip=t.price,
        #     position=NavigationItemPosition.BOTTOM
        # )


        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1200, 960)
        self.setMinimumHeight(960)
        self.setMinimumWidth(1200)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('AI Store')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def initWidget(self):
        self.stackedWidget.addWidget(self.appInterface)


    def init_data(self):
        self.init_homeInterface()
        

    def init_homeInterface(self):
        registy = read_all_installed_software_from_registry(REGISTY_PATH)
        self.homeInterface.set_registy(registy)
        # self.homeInterface.set_apps_state()
        self.homeInterface.refresh()

    def onInitFinished(self):
        if cfg.get(cfg.checkUpdateAtStartUp):
            self.update_manager = UpdateManager(self, start_up=True)
            self.update_manager.check_for_updates()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(HELP_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

    def switchToAppInterface(self, app_card):
        self.appInterface.update_window(app_card)
        self.stackedWidget.setCurrentWidget(self.appInterface, False)

    # def check_software_registy(self):
    #     signalBus.software_registySig.emit(self.software_list)

    # def software_uninstall(self, app_card):
    #     print(app_card.name)
    #     title = self.tr('Uninstall ' + app_card.name)
    #     content = self.tr(f"Do you want to uninstall {app_card.name} ?")
    #     w = MessageBox(title, content, self)
    #     if w.exec():
            
    #         for item in self.software_list:
    #             if item["DisplayName"] == app_card.name:
    #                 self.software_list.remove(item)
    #         app_card.refreshSig.emit()

    #         for item in self.software_list:
    #             print(item)

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)
        # signalBus.software_uninstallSig.connect(self.software_uninstall)
        signalBus.switchToAppInterfaceSig.connect(
            self.switchToAppInterface)