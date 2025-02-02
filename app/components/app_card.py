# coding:utf-8
import random
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,QPushButton, QSpacerItem, QSizePolicy

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, CardWidget,PushButton,PrimaryPushButton,ProgressRing,SimpleCardWidget,InfoBar, InfoBarIcon, FluentIcon, InfoBarPosition,SmoothScrollArea

from app.common.logger import logger
from app.common.trie import Trie
from app.database.entity.app_info import AppInfo
from app.database.library import Library
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
import importlib
from qfluentwidgets import MessageBox

from app.core.typing import AppState

class AppCard(CardWidget):
    """ Sample card """
    refreshSig = pyqtSignal()
    stateChangedSig = pyqtSignal(object)

    def __init__(self, library: Library, app_info: AppInfo, routeKey, index, state: AppState, parent=None):
        super().__init__(parent=parent)
        self.library = library
        self.app_info = app_info
        # self.process = None

        self.index = index
        self.routeKey = routeKey

        self.brief_introduction = app_info.brief_introduction
        self.description = app_info.description

        self.state: AppState =  state

        self.iconWidget = IconWidget(self.app_info.icon, self)
        self.titleLabel = QLabel(self.app_info.title, self)
        self.brief_introductionLabel = QLabel(TextWrap.wrap(self.brief_introduction, 80, False)[0], self)

        self.button_install = PrimaryPushButton(self.tr('Install'), self)
        self.button_install.setFixedSize(100, 30)

        self.ring = ProgressRing(self)
        self.ring.setFixedSize(50, 50)
        self.ring.setTextVisible(True)
        self.ring.setVisible(False)


        self.button_run = PrimaryPushButton(self.tr('Run'), self)
        self.button_run.setVisible(False)
        self.button_run.setFixedSize(100, 30)

        self.button_stop = PrimaryPushButton(self.tr('Stop'), self)
        self.button_stop.setVisible(False)
        self.button_stop.setFixedSize(100, 30)

        self.button_uninstall = PushButton(self.tr('Uninstall'), self)
        self.button_uninstall.setVisible(False)
        self.button_uninstall.setFixedSize(100, 30)


        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.vbuttonLayout = QVBoxLayout()
        # self.vbuttonLayout.setContentsMargins(0, 20, 0, 20)

        self.setFixedSize(500, 120)
        # self.setFixedSize(500, 90)

        self.iconWidget.setFixedSize(48, 48)

        self.initLayout()
        self.connectSignalToSlot()

        self.titleLabel.setObjectName('titleLabel')
        # self.brief_introductionLabel.setObjectName('contentLabel')
        self.brief_introductionLabel.setObjectName('briefIntroduction')

        self.refresh()

    def initLayout(self):
        self.vbuttonLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 20, 20,20)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addWidget(self.button_install)
        self.hBoxLayout.addWidget(self.ring)


        self.vbuttonLayout.addWidget(self.button_run)
        self.vbuttonLayout.addWidget(self.button_stop)
        self.vbuttonLayout.addWidget(self.button_uninstall)
        self.hBoxLayout.addLayout(self.vbuttonLayout)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.brief_introductionLabel)
        self.vBoxLayout.addStretch(1)

    def on_button_clicked(self):
        app_version = self.library.app_versions_controller.get_last_app_version_by_app_id(self.app_info.id)
        signalBus.software_installSig.emit(self, app_version)

    def on_button_uninstall_clicked(self):
        signalBus.software_uninstallSig.emit(self)

    def on_button_run_clicked(self):
        signalBus.software_runSig.emit(self)

    def on_button_stop_clicked(self):
        signalBus.software_stopSig.emit(self)

    def update_progress_bar(self, file, value):
        # 更新进度条
        self.ring.setValue(value)

    def set_state(self, state : AppState):
        self.state = state
        self.stateChangedSig.emit(self.state)

    def refresh(self):
        # instlled
        if self.state == 'installed' or self.state == 'install_completed' or self.state == 'stop':
            self.button_install.setVisible(False)
            self.ring.setVisible(False)
            self.button_run.setVisible(True)
            self.button_stop.setVisible(False)
            self.button_uninstall.setVisible(True)
            self.ring.setValue(0)

        elif self.state == 'uninstall' or self.state == 'uninstall_completed':
            self.button_install.setVisible(True)
            self.ring.setVisible(False)
            self.button_run.setVisible(False)
            self.button_stop.setVisible(False)
            self.button_uninstall.setVisible(False)
            self.ring.setValue(0)

        elif self.state == 'installing':
            self.button_install.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_stop.setVisible(False)
            self.button_uninstall.setVisible(False)
        elif self.state == 'uninstalling':
            self.button_install.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_stop.setVisible(False)
            self.button_uninstall.setVisible(False)
        elif self.state == 'running':
            self.button_install.setVisible(False)
            self.ring.setVisible(False)
            self.button_run.setVisible(False)
            self.button_stop.setVisible(True)
            self.button_uninstall.setVisible(False)
        # elif self.install_state == 'uninstall'

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        # signalBus.switchToSampleCard.emit(self.routeKey, self.index)
        signalBus.switchToAppInterfaceSig.emit(self)

    def is_install(self, software_list):
        for item in software_list:
            if item['DisplayName'] == self.app_info:
                self.ring.setVisible(False)
                self.button_run.setVisible(True)
                self.button_stop.setVisible(False)
                self.button_uninstall.setVisible(True)
            else:
                pass
    
    def connectSignalToSlot(self):
        
        self.button_install.clicked.connect(self.on_button_clicked)
        self.button_run.clicked.connect(self.on_button_run_clicked)
        self.button_stop.clicked.connect(self.on_button_stop_clicked)
        self.button_uninstall.clicked.connect(self.on_button_uninstall_clicked)

        signalBus.software_registrySig.connect(self.is_install)

        self.refreshSig.connect(self.refresh)
        
class AppCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.cards = []
        self.trie = Trie()
        
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.__initWidget()


    def __initWidget(self):
        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)


        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.__setQss()


    def __setQss(self):
        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.APP_CARD.apply(self)

    def addAppCard(self, library: Library, app_info: AppInfo, state: AppState, routeKey, index):
        """ add app card """
        card = AppCard(library, app_info, routeKey, index, state,  self)

        self.trie.insert(app_info.title.replace(" ", "").replace("_", ""), len(self.cards))
        self.cards.append(card)
        self.flowLayout.addWidget(card)

    def refresh(self):
        count = self.flowLayout.count()
        for index in range(count):
            self.flowLayout.itemAt(index).widget().refresh()

    def showAllApps(self):
        self.flowLayout.removeAllWidgets()
        for card in self.cards:
            card.show()
            self.flowLayout.addWidget(card)

        self.flowLayout.update()
        

    def search(self, keyWord: str):
        logger.info(f"search application keyWord: {keyWord}")
        items = self.trie.items(keyWord.lower())
        indexes = {i[1] for i in items}
        self.flowLayout.removeAllWidgets()

        for i, card in enumerate(self.cards):
            isVisible = card.isVisible() and i in indexes
            card.setVisible(isVisible)
            if isVisible:
                self.flowLayout.addWidget(card)

        self.flowLayout.update()
        
    def filter_installed(self, installed_checkbox: bool):
        logger.info(f"show installed application : {installed_checkbox}")
        self.flowLayout.removeAllWidgets()

        for card in self.cards:
            isVisible = card.isVisible() and card.state == "installed" or card.state == "running" or card.state == "stop"
            card.setVisible(isVisible)
            if isVisible:
                self.flowLayout.addWidget(card)

        self.flowLayout.update()
