# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,QPushButton, QSpacerItem, QSizePolicy

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, CardWidget,PushButton,PrimaryPushButton,ProgressRing
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
import importlib
from qfluentwidgets import MessageBox

from app.core.typing import AppState

class AppCard(CardWidget):
    """ Sample card """
    refreshSig = pyqtSignal()

    def __init__(self, icon, title, content, routeKey, index, name, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.routeKey = routeKey
        self.name = name

        self.state: AppState =  'uninstall'

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)

        self.button = PrimaryPushButton(self.tr('Install'), self)
        self.button.setFixedSize(100, 30)

        self.ring = ProgressRing(self)
        self.ring.setFixedSize(50, 50)
        self.ring.setTextVisible(True)
        self.ring.setVisible(False)


        self.button_run = PrimaryPushButton(self.tr('Run'), self)
        self.button_run.setVisible(False)
        self.button_run.setFixedSize(100, 30)

        self.button_uninstall = PushButton(self.tr('Uninstall'), self)
        self.button_uninstall.setVisible(False)
        self.button_uninstall.setFixedSize(100, 30)


        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.vbuttonLayout = QVBoxLayout()
        self.vbuttonLayout.setAlignment(Qt.AlignVCenter)
        # self.vbuttonLayout.setContentsMargins(0, 20, 0, 20)

        self.setFixedSize(500, 120)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 20, 20,20)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addWidget(self.button)
        self.hBoxLayout.addWidget(self.ring)


        self.vbuttonLayout.addWidget(self.button_run)
        self.vbuttonLayout.addWidget(self.button_uninstall)
        self.hBoxLayout.addLayout(self.vbuttonLayout)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

        self.button.clicked.connect(self.on_button_clicked)
        self.button_run.clicked.connect(self.on_button_run_clicked)
        self.button_uninstall.clicked.connect(self.on_button_uninstall_clicked)

        signalBus.software_registySig.connect(self.is_install)

        self.refreshSig.connect(self.refresh)

    def on_button_clicked(self):
        signalBus.software_installSig.emit(self)

    def on_button_uninstall_clicked(self):
        signalBus.software_uninstallSig.emit(self)

    def on_button_run_clicked(self):
        signalBus.software_runSig.emit(self)

    def update_progress_bar(self, file, value):
        # 更新进度条
        self.ring.setValue(value)

    def set_state(self, state : AppState):
        self.state = state

    def refresh(self):
        # instlled
        if self.state == 'installed' or self.state == 'install_completed':
            self.button.setVisible(False)
            self.ring.setVisible(False)
            self.button_run.setVisible(True)
            self.button_uninstall.setVisible(True)
            self.ring.setValue(0)

        elif self.state == 'uninstall' or self.state == 'uninstall_completed':
            self.button.setVisible(True)
            self.ring.setVisible(False)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)
            self.ring.setValue(0)

        elif self.state == 'installing':
            self.button.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)
        elif self.state == 'uninstalling':
            self.button.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)
        # elif self.install_state == 'uninstall'

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self.routeKey, self.index)

    def is_install(self, software_list):
        for item in software_list:
            if item['DisplayName'] == self.name:
                self.ring.setVisible(False)
                self.button.setVisible(False)
                self.button_run.setVisible(True)
                self.button_uninstall.setVisible(True)
            else:
                pass
        
class AppCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        StyleSheet.SAMPLE_CARD.apply(self)

    def addAppCard(self, icon, title, content, routeKey, index,name):
        """ add app card """
        card = AppCard(icon, title, content, routeKey, index, name, self)
        self.flowLayout.addWidget(card)

    def refresh(self):
        count = self.flowLayout.count()
        for index in range(count):
            self.flowLayout.itemAt(index).widget().refresh()