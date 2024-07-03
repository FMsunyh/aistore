# coding:utf-8
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect,QSpacerItem,QSizePolicy

from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, FluentIcon, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, ProgressRing,ProgressBar,MessageBox)

from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush

from app.components.app_card import AppCard
from app.core.typing import AppState
from ..common.signal_bus import signalBus

from app.database.entity.app_info import AppInfo
from app.database.library import Library

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class AppInfoCard(SimpleCardWidget):
    """ App information card """

    def __init__(self, app_info: AppInfo=None, parent=None):
        super().__init__(parent)
        self.app_info = app_info
        # self.icon_label = ImageLabel(":/qfluentwidgets/images/logo.png", self)
        self.icon_label = ImageLabel(self.app_info.icon, self)
        self.icon_label.setBorderRadius(8, 8, 8, 8)
        self.icon_label.scaledToWidth(120)

        self.state: AppState =  'uninstall'

        self.nameLabel = TitleLabel(f'{self.app_info.name}', self)

        self.button_install = PrimaryPushButton(self.tr('Install'), self)


        self.ring = ProgressBar(self)
        self.ring.setFixedWidth(200)  
        self.ring.setFixedHeight(20)
        # self.ring.setFixedSize(200, 20)
        self.ring.setTextVisible(True)
        self.ring.setVisible(False)

        self.button_run = PrimaryPushButton(self.tr('Run'), self)
        self.button_run.setFixedWidth(160)

        self.button_uninstall = PushButton(self.tr('Uninstall'), self)
        self.button_uninstall.setFixedWidth(160)


        self.companyLabel = HyperlinkLabel(
            QUrl('https://www.zjusmart.com/#/'), 'ZhongJuYun Inc.', self)
        self.button_install.setFixedWidth(160)

        self.scoreWidget = StatisticsWidget(self.tr('RATINGS'), '5.0', self)
        self.separator = VerticalSeparator(self)
        self.commentWidget = StatisticsWidget(self.tr('REVIEWS'), '3K', self)

        self.brief_introductionLabel = BodyLabel(f'{self.app_info.brief_introduction}', self)
        self.brief_introductionLabel.setWordWrap(True)

        self.tagButton = PillPushButton(self.tr('Component Library'), self)
        self.tagButton.setCheckable(False)
        setFont(self.tagButton, 12)
        self.tagButton.setFixedSize(130, 32)

        self.shareButton = TransparentToolButton(FluentIcon.SHARE, self)
        self.shareButton.setFixedSize(32, 32)
        self.shareButton.setIconSize(QSize(14, 14))

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        self.hbuttonLayout = QHBoxLayout()

        self.initLayout()

        self.button_install.clicked.connect(self.on_button_clicked)
        self.button_run.clicked.connect(self.on_button_run_clicked)
        self.button_uninstall.clicked.connect(self.on_button_uninstall_clicked)


    def initLayout(self):
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.icon_label)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # name label and install button
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.nameLabel)
        self.topLayout.addWidget(self.button_install, 0, Qt.AlignRight)
        self.topLayout.addWidget(self.ring, 0, Qt.AlignRight)


        self.hbuttonLayout.setSpacing(20)
        self.hbuttonLayout.setAlignment(Qt.AlignVCenter)
        self.hbuttonLayout.addWidget(self.button_run)
        self.hbuttonLayout.addWidget(self.button_uninstall)

        self.topLayout.addLayout(self.hbuttonLayout)

        # company label
        self.vBoxLayout.addSpacing(3)
        self.vBoxLayout.addWidget(self.companyLabel)

        # statistics widgets
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(10)
        self.statisticsLayout.addWidget(self.scoreWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.commentWidget)
        self.statisticsLayout.setAlignment(Qt.AlignLeft)

        
        # description label
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.brief_introductionLabel)

        # button
        self.vBoxLayout.addSpacing(12)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.tagButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.shareButton, 0, Qt.AlignRight)

    def update_window(self, app_card : AppCard):
        self.app_card = app_card

        self.icon_label.setImage(self.app_card.app_info.icon) 
        self.nameLabel.setText(f'{self.app_card.app_info.title}')
        self.brief_introductionLabel.setText(f'{self.app_card.app_info.brief_introduction}')
        self.state = self.app_card.state
        
        self.app_card.stateChangedSig.connect(self.set_state)
        self.app_card.refreshSig.connect(self.refresh)
        self.app_card.ring.valueChanged.connect(self.ring.setValue)

        self.refresh()

    def on_button_clicked(self):
        signalBus.software_installSig.emit(self.app_card)

    def on_button_uninstall_clicked(self):
        signalBus.software_uninstallSig.emit(self.app_card)

    def on_button_run_clicked(self):
        signalBus.software_runSig.emit(self.app_card)

    # def update_progress_bar(self, file, value):
    #     # 更新进度条
    #     self.ring.setValue(value)

    def set_state(self, state : AppState):
        self.state = state

    def refresh(self):
        # instlled
        if self.state == 'installed' or self.state == 'install_completed':
            self.button_install.setVisible(False)
            self.ring.setVisible(False)
            self.button_run.setVisible(True)
            self.button_uninstall.setVisible(True)
            self.ring.setValue(0)

        elif self.state == 'uninstall' or self.state == 'uninstall_completed':
            self.button_install.setVisible(True)
            self.ring.setVisible(False)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)
            self.ring.setValue(0)

        elif self.state == 'installing':
            self.button_install.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)
        elif self.state == 'uninstalling':
            self.button_install.setVisible(False)
            self.ring.setVisible(True)
            self.button_run.setVisible(False)
            self.button_uninstall.setVisible(False)


class GalleryCard(HeaderCardWidget):
    """ Gallery card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr('Screenshots'))

        self.flipView = HorizontalFlipView(self)
        self.expandButton = TransparentToolButton(
            FluentIcon.CHEVRON_RIGHT_MED, self)

        self.expandButton.setFixedSize(32, 32)
        self.expandButton.setIconSize(QSize(12, 12))

        self.flipView.addImages([
            ":/gallery/images/Shoko1.jpg",
            ":/gallery/images/Shoko2.jpg",
            ":/gallery/images/Shoko3.jpg",
            ":/gallery/images/Shoko4.jpg",
        ])
        self.flipView.setBorderRadius(8)
        self.flipView.setSpacing(10)

        self.headerLayout.addWidget(self.expandButton, 0, Qt.AlignRight)
        self.viewLayout.addWidget(self.flipView)

class WhatsNewCard(HeaderCardWidget):
    """ Description card """

    def __init__(self, library: Library = None, app_info: AppInfo=None, title: str='', parent=None):
        super().__init__(parent)
        self.library = library

        self.title = title
        app_version = self.library.app_versions_controller.get_last_app_version_by_app_id(app_info.id)
        self.versionWidget = HStatisticsWidget(self.tr('Version'), app_version.version_number, app_version.release_date, self)
        self.descriptionLabel = BodyLabel(
            self.tr(f'{app_version.change_log}'), self)

        self.descriptionLabel.setWordWrap(True)
        self.vBoxLayout.insertWidget(2, self.versionWidget)

        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle(self.tr(f'{self.title}'))

    def set_description(self, value):
        self.descriptionLabel.setText(value)

    def update_window(self, app_info: AppInfo=None):
        if app_info is None:
            return
        
        app_info = app_info
        app_version = self.library.app_versions_controller.get_last_app_version_by_app_id(app_info.id)

        self.versionWidget.update_window(self.tr('Version'), app_version.version_number, app_version.release_date)
        self.set_description(self.tr(f'{app_version.change_log}'))

class DescriptionCard(HeaderCardWidget):
    """ Description card """

    def __init__(self, title, description, parent=None):

        super().__init__(parent)
        self.title = title
        self.description = description
        self.descriptionLabel = BodyLabel(
            self.tr(f'{self.description}'), self)

        self.descriptionLabel.setWordWrap(True)
        self.viewLayout.addWidget(self.descriptionLabel)
        self.setTitle(self.tr(f'{self.title}'))

    def set_title(self, title):
        self.title = title
        
    def set_description(self, description):
        self.description = description

    def update_window(self,):
        pass
class SystemRequirementCard(HeaderCardWidget):
    """ System requirements card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr('System Requirements'))
        self.infoLabel = BodyLabel(self.tr('windows 10'), self)
        self.successIcon = IconWidget(InfoBarIcon.SUCCESS, self)
        self.detailButton = HyperlinkLabel(self.tr('Details'), self)

        self.vBoxLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()

        self.successIcon.setFixedSize(16, 16)
        self.hBoxLayout.setSpacing(10)
        self.vBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.hBoxLayout.addWidget(self.successIcon)
        self.hBoxLayout.addWidget(self.infoLabel)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.detailButton)

        self.viewLayout.addLayout(self.vBoxLayout)


class LightBox(QWidget):
    """ Light box """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        if isDarkTheme():
            tintColor = QColor(32, 32, 32, 200)
        else:
            tintColor = QColor(255, 255, 255, 160)

        self.acrylicBrush = AcrylicBrush(self, 30, tintColor, QColor(0, 0, 0, 0))

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni = QPropertyAnimation(self.opacityEffect, b"opacity", self)
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)

        self.vBoxLayout = QVBoxLayout(self)
        self.closeButton = TransparentToolButton(FluentIcon.CLOSE, self)
        self.flipView = HorizontalFlipView(self)
        self.nameLabel = BodyLabel(self.tr('Screenshots 1'), self)
        self.pageNumButton = PillPushButton('1 / 4', self)

        self.pageNumButton.setCheckable(False)
        self.pageNumButton.setFixedSize(80, 32)
        setFont(self.nameLabel, 16, QFont.DemiBold)

        self.closeButton.setFixedSize(32, 32)
        self.closeButton.setIconSize(QSize(14, 14))
        self.closeButton.clicked.connect(self.fadeOut)

        self.vBoxLayout.setContentsMargins(26, 28, 26, 28)
        self.vBoxLayout.addWidget(self.closeButton, 0, Qt.AlignRight | Qt.AlignTop)
        self.vBoxLayout.addWidget(self.flipView, 1)
        self.vBoxLayout.addWidget(self.nameLabel, 0, Qt.AlignHCenter)
        self.vBoxLayout.addSpacing(10)
        self.vBoxLayout.addWidget(self.pageNumButton, 0, Qt.AlignHCenter)

        self.flipView.addImages([
            ":/gallery/images/Shoko1.jpg",
            ":/gallery/images/Shoko2.jpg",
            ":/gallery/images/Shoko3.jpg",
            ":/gallery/images/Shoko4.jpg",
        ])
        self.flipView.currentIndexChanged.connect(self.setCurrentIndex)

    def setCurrentIndex(self, index: int):
        self.nameLabel.setText(self.tr('Screenshots') + f' {index + 1}')
        self.pageNumButton.setText(f'{index + 1} / {self.flipView.count()}')
        self.flipView.setCurrentIndex(index)

    def paintEvent(self, e):
        if self.acrylicBrush.isAvailable():
            return self.acrylicBrush.paint()

        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        if isDarkTheme():
            painter.setBrush(QColor(32, 32, 32))
        else:
            painter.setBrush(QColor(255, 255, 255))

        painter.drawRect(self.rect())

    def resizeEvent(self, e):
        w = self.width() - 52
        self.flipView.setItemSize(QSize(w, w * 9 // 16))

    def fadeIn(self):
        rect = QRect(self.mapToGlobal(QPoint()), self.size())
        self.acrylicBrush.grabImage(rect)

        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(150)
        self.opacityAni.start()
        self.show()

    def fadeOut(self):
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.setDuration(150)
        self.opacityAni.finished.connect(self._onAniFinished)
        self.opacityAni.start()

    def _onAniFinished(self):
        self.opacityAni.finished.disconnect()
        self.hide()

    def update_window(self,):
        pass

class StatisticsWidget(QWidget):
    """ Statistics widget """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignBottom)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

class HStatisticsWidget(QWidget):
    """ Statistics widget """

    def __init__(self, title: str, value: str, release_date: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.release_dateLabel = BodyLabel(release_date, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(24, 0, 24, 0)
        self.hBoxLayout.addWidget(self.titleLabel)
        self.hBoxLayout.addWidget(self.valueLabel)
        self.hBoxLayout.addItem(QSpacerItem(24, 24, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.hBoxLayout.addWidget(self.release_dateLabel)

        setFont(self.valueLabel, 18, QFont.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

    def set_title(self, title):
        self.titleLabel.setText(title)

    def set_value(self, value):
        self.valueLabel.setText(value)

    def set_release_date(self, value):
        self.release_dateLabel.setText(value)

    def update_window(self, title, value, release_date):
        self.set_title(title)
        self.set_value(value)
        self.set_release_date(release_date)

class AppInterface(SingleDirectionScrollArea):

    def __init__(self, library: Library = None, app_info: AppInfo=None, parent=None):
        super().__init__(parent)

        self.library = library
        self.app_info = app_info

        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.appInfoCard = AppInfoCard(self.app_info, self)
        self.whatNewCard = WhatsNewCard(self.library, app_info, 'What\'s New', self)
        self.galleryCard = GalleryCard(self)
        self.descriptionCard = DescriptionCard(self.tr('Description'), self.tr('Description of app details'), self)
        self.systemCard = SystemRequirementCard(self)

        self.lightBox = LightBox(self)
        self.lightBox.hide()
        self.galleryCard.flipView.itemClicked.connect(self.showLightBox)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("appInterface")

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.appInfoCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.whatNewCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.galleryCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.descriptionCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(self.systemCard, 0, Qt.AlignTop)

        self.setStyleSheet("QScrollArea {border: none; background:transparent}")
        self.view.setStyleSheet('QWidget {background:transparent}')

    def showLightBox(self):
        index = self.galleryCard.flipView.currentIndex()
        self.lightBox.setCurrentIndex(index)
        self.lightBox.fadeIn()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.lightBox.resize(self.size())

    def update_window(self, app_card : AppCard):
        self.appInfoCard.update_window(app_card)
        self.whatNewCard.update_window(app_card.app_info)