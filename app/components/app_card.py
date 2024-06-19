# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout,QPushButton

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, CardWidget,PushButton,PrimaryPushButton,ProgressRing
from ..common.signal_bus import signalBus
from ..common.style_sheet import StyleSheet
import importlib


class AppCard(CardWidget):
    """ Sample card """
    install_clicked = pyqtSignal(object,object)
    ring_value_changed = pyqtSignal(int)
    install_finished = pyqtSignal()

    def __init__(self, icon, title, content, routeKey, index, name, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.routeKey = routeKey
        self.name = name

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 45, False)[0], self)

        self.button = PrimaryPushButton('Install', self)
        self.button.setFixedSize(100, 30)

        self.ring = ProgressRing(self)
        self.ring.setFixedSize(50, 50)
        self.ring.setTextVisible(True)
        self.ring.setVisible(False)


        self.button_uninstall = PrimaryPushButton('Uninstall', self)
        self.button_uninstall.setVisible(False)
        self.button_uninstall.setFixedSize(100, 30)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(500, 90)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 20, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.hBoxLayout.addWidget(self.button)
        self.hBoxLayout.addWidget(self.ring)
        self.hBoxLayout.addWidget(self.button_uninstall)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

        self.button.clicked.connect(self.on_button_clicked)
        self.ring_value_changed.connect(self.update_progress_bar)
        self.install_finished.connect(self.on_finished)
        # signalBus.progressSig.connect(self.update_progress_bar)

    def on_button_clicked(self):
        self.button.setVisible(False)
        self.ring.setVisible(True)
        self.install_clicked.emit(self.ring_value_changed,self.install_finished)
        # self.simulate_installation()

    def update_progress_bar(self, value):
        # 更新进度条
        self.ring.setValue(value)
        if value==100:
            self.ring.setVisible(False)
            self.button_uninstall.setVisible(True)
        # self.ring.setValue(50)

    def on_finished(self):
        self.ring.setVisible(False)
        self.button_uninstall.setVisible(True)
        self.button.setEnabled(False)

    def simulate_installation(self):
        # 模拟安装进度
        import time
        from threading import Thread

        def run():
            for i in range(101):
                time.sleep(0.05)
                self.ring.setValue(i)

        # 使用线程来模拟进度条的更新
        thread = Thread(target=run)
        thread.start()
    # def openDir(self):
    #     print("Hello World")
    #     installer_module = importlib.import_module('app.installer.'+ self.routeKey)
    #     installer_module.pre_check()

    # def mouseReleaseEvent(self, e):
    #     super().mouseReleaseEvent(e)
    #     signalBus.switchToSampleCard.emit(self.routeKey, self.index)


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
