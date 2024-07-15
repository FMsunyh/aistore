'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-16 05:28:37
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-15 11:47:00
FilePath: \aistore\app\view\main_window.py
Description: main windows
'''
# coding: utf-8
from PyQt5.QtCore import QUrl, QSize,Qt
from PyQt5.QtGui import QIcon, QDesktopServices, QColor
from PyQt5.QtWidgets import QApplication,qApp
from PyQt5.QtSql import QSqlDatabase

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF

from app.common.icon import Icon
from app.core.registry import read_all_installed_software_from_registry
from app.core.update import UpdateManager
from app.database.db_initializer import DBInitializer
from app.database.library import Library
from app.view.app_interface import AppInterface
from app.view.model_interface import ModelInterface
from app.view.model_library_interface import SDModelInterface, ComfyUIModelInterface

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
        self.init_data()

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

        self.onInitFinished()
    
    def createWidgets(self):
        # create sub interface
        self.homeInterface = HomeInterface(library = self.library, registry=self.registry, parent=self)
        self.navigationViewInterface = NavigationViewInterface(self)
        self.modelInterface = ModelInterface(self)
        self.settingInterface = SettingInterface(self)

        if len(self.library.app_infos) > 0:
            app_info = self.library.app_infos[0]
            self.appInterface = AppInterface(library = self.library, app_info = app_info, parent=self)
        
        self.sdModelInterface = SDModelInterface(library = self.library, registry=self.registry, parent=self)
        self.comfyuiModelInterface = ComfyUIModelInterface(self)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))


        # self.addSubInterface(self.aistoreInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        
        # self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.modelInterface, Icon.EMOJI_TAB_SYMBOLS,t.model, pos)
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
        self.stackedWidget.addWidget(self.sdModelInterface)
        self.stackedWidget.addWidget(self.comfyuiModelInterface)

    def init_data(self):
        DBInitializer.init()
        self.library = Library(QSqlDatabase.database(DBInitializer.CONNECTION_NAME))
    
        self.registry = read_all_installed_software_from_registry(REGISTY_PATH)

    def onInitFinished(self):
        if cfg.get(cfg.checkUpdateAtStartUp):
            self.update_manager = UpdateManager(self, start_up=True)
            self.update_manager.check_for_updates()

    def onAppMessage(self, message: str):
        if message == "show":
            if self.windowState() & Qt.WindowMinimized:
                self.showNormal()
            else:
                self.show()
        else:
            # self.setPlaylist(self.library.loadFromFiles([message]))
            self.show()

    def onAppError(self, message: str):
        """ app error slot """
        qApp.clipboard().setText(message)
        w = MessageBox(
            self.tr("Unhandled exception occurred"),
            self.tr(
                "The error message has been written to the paste board and log. Do you want to report?"),
            self)
        w.hideCancelButton()
        w.exec()
        

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(HELP_URL))
        else:
            QDesktopServices.openUrl(QUrl(HELP_URL))

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

    def switchToModelLibraryInterface(self, app_card):

        # self.appInterface.update_window(app_card)
        # self.stackedWidget.setCurrentWidget(self.modelInterface, False)
        if app_card.app_info.name == 'sd_webui':
            self.stackedWidget.setCurrentWidget(self.sdModelInterface, False)

        if app_card.app_info.name == 'comfyui':
            self.stackedWidget.setCurrentWidget(self.comfyuiModelInterface, False)

    def switchToAppInterface(self, app_card):
        self.appInterface.update_window(app_card)
        self.stackedWidget.setCurrentWidget(self.appInterface, False)
    

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)
        # signalBus.software_uninstallSig.connect(self.software_uninstall)
        signalBus.switchToAppInterfaceSig.connect(self.switchToAppInterface)
        signalBus.switchToModelLibraryInterfaceSig.connect(self.switchToModelLibraryInterface)

        signalBus.appMessageSig.connect(self.onAppMessage)
        signalBus.appErrorSig.connect(self.onAppError)