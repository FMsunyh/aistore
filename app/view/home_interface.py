# coding:utf-8
import importlib
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon,MessageBox

from app.components.app_card import AppCardView
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet
from ..common.signal_bus import signalBus

class BannerWidget(QWidget):
    """ Banner widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('AI Store', self)
        self.banner = QPixmap(':/gallery/images/header1.png')
        self.linkCardView = LinkCardView(self)

        self.galleryLabel.setObjectName('galleryLabel')
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        self.vBoxLayout.addWidget(self.linkCardView, 1, Qt.AlignBottom)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.linkCardView.addCard(
            ':/gallery/images/logo.png',
            self.tr('Getting started'),
            self.tr('An overview of app development options and samples.'),
            HELP_URL
        )

        self.linkCardView.addCard(
            ':/gallery/images/h100.png',
            self.tr('GPU Lab'),
            self.tr(
                'The latest fluent design controls and styles for your applications.'),
            REPO_URL
        )

        self.linkCardView.addCard(
            FluentIcon.CODE,
            self.tr('Code samples'),
            self.tr(
                'Find samples that demonstrate specific tasks, features and APIs.'),
            EXAMPLE_URL
        )

        self.linkCardView.addCard(
            FluentIcon.FEEDBACK,
            self.tr('Send feedback'),
            self.tr('Help us improve PyQt-Fluent-Widgets by providing feedback.'),
            FEEDBACK_URL
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    """ Home interface """

    def __init__(self, registry=None, parent=None):
        super().__init__(parent=parent)

        self.registry = registry

        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        self.loadApps()
        self.__connectSignalToSlot()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

    def loadApps(self):
        """ load apps """

        # Popular Tools
        self.popularView = AppCardView(self.tr('Popular Tools'), self.view)
        self.popularView.addAppCard(
            icon=":/gallery/images/controls/MenuFlyout.png",
            title="FaceFusion",
            content=self.tr(
                "Shows a contextual list of simple commands or options."),
            routeKey="menuInterface",
            index=0,
            name="facefusion"
        )

        self.popularView.addAppCard(
            icon=":/gallery/images/controls/CommandBar.png",
            title="kohya_ss",
            content=self.tr(
                "Shows a contextual list of simple commands or options."),
            routeKey="menuInterface",
            index=3,
            name="kohya_ss"
        )
        self.popularView.addAppCard(
            icon=":/gallery/images/controls/CommandBarFlyout.png",
            title="sd_webui",
            content=self.tr(
                "A mini-toolbar displaying proactive commands, and an optional menu of commands."),
            routeKey="menuInterface",
            index=7,
            name="sd_webui"
        )
        self.vBoxLayout.addWidget(self.popularView)

    def set_registy(self, registy):
        self.registy = registy


    def set_apps_state(self):
        count =  self.popularView.flowLayout.count()
        print(count)
        for index in range(count):
            app_name = self.popularView.flowLayout.itemAt(index).widget().name
            for item in self.registy:
                if item["DisplayName"] == app_name:
                    self.popularView.flowLayout.itemAt(index).widget().set_install_state(True)


    def _aboutCardClick(self):
        print("__connectSignalToSlot")


    def __connectSignalToSlot(self):

        count =  self.popularView.flowLayout.count()
        print(count)
        for index in range(count):

            print(self.popularView.flowLayout.itemAt(index).widget().routeKey)
            print(self.popularView.flowLayout.itemAt(index).widget().index)
            print(self.popularView.flowLayout.itemAt(index).widget().name)

            installer_name = self.popularView.flowLayout.itemAt(index).widget().name
            installer_module = importlib.import_module('app.installer.'+ installer_name)
            self.popularView.flowLayout.itemAt(index).widget().install_clicked.connect(installer_module.process)

        signalBus.software_uninstallSig.connect(self.software_uninstall)
            # self.popularView.flowLayout.itemAt(index).widget().install_clicked.connect(installer_module.process)

    def software_uninstall(self, app_card):
        app_name = app_card.name
        print(app_card.name)

        title = self.tr('Uninstall ' + app_card.name)
        content = self.tr(f"Do you want to uninstall {app_card.name} ?")
        w = MessageBox(title, content, self)

        if w.exec():
            installer_module = importlib.import_module('app.installer.'+ app_name)
            installer_module.uninstall(self.registry)

                        
            for item in self.registry:
                if item["DisplayName"] == app_card.name:
                    self.registry.remove(item)
            
            for item in self.registry:
                print(item)

            app_card.refreshSig.emit()

    def refresh(self):
        self.popularView.refresh()
        
            