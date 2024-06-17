# coding:utf-8
import importlib
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon

from app.components.app_card import AppCardView
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet


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

    def __init__(self, parent=None):
        super().__init__(parent=parent)
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

        """
        # # AI Image Tools
        # basicInputView = SampleCardView(
        #     self.tr("AI Image Tools"), self.view)
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/Button.png",
        #     title="Stable diffusion WebUI",
        #     content=self.tr(
        #         "A control that responds to user input and emit clicked signal."),
        #     routeKey="sd_webui",
        #     index=0
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/Checkbox.png",
        #     title="FaceFusion",
        #     content=self.tr("A control that a user can select or clear."),
        #     routeKey="facefusion",
        #     index=8
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/ComboBox.png",
        #     title="Kohya_ss GUI",
        #     content=self.tr(
        #         "A drop-down list of items a user can select from."),
        #     routeKey="kohya_ss",
        #     index=10
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/DropDownButton.png",
        #     title="ananconda",
        #     content=self.tr(
        #         "A button that displays a flyout of choices when clicked."),
        #     routeKey="ananconda",
        #     index=12
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/HyperlinkButton.png",
        #     title="HyperlinkButton",
        #     content=self.tr(
        #         "A button that appears as hyperlink text, and can navigate to a URI or handle a Click event."),
        #     routeKey="basicInputInterface",
        #     index=18
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/RadioButton.png",
        #     title="RadioButton",
        #     content=self.tr(
        #         "A control that allows a user to select a single option from a group of options."),
        #     routeKey="basicInputInterface",
        #     index=19
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/Slider.png",
        #     title="Slider",
        #     content=self.tr(
        #         "A control that lets the user select from a range of values by moving a Thumb control along a track."),
        #     routeKey="basicInputInterface",
        #     index=20
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/SplitButton.png",
        #     title="SplitButton",
        #     content=self.tr(
        #         "A two-part button that displays a flyout when its secondary part is clicked."),
        #     routeKey="basicInputInterface",
        #     index=21
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/ToggleSwitch.png",
        #     title="SwitchButton",
        #     content=self.tr(
        #         "A switch that can be toggled between 2 states."),
        #     routeKey="basicInputInterface",
        #     index=25
        # )
        # basicInputView.addSampleCard(
        #     icon=":/gallery/images/controls/ToggleButton.png",
        #     title="ToggleButton",
        #     content=self.tr(
        #         "A button that can be switched between two states like a CheckBox."),
        #     routeKey="basicInputInterface",
        #     index=26
        # )
        # self.vBoxLayout.addWidget(basicInputView)

        # # AI Video Tools
        # dateTimeView = SampleCardView(self.tr('AI Video Tools'), self.view)
        # dateTimeView.addSampleCard(
        #     icon=":/gallery/images/controls/CalendarDatePicker.png",
        #     title="CalendarPicker",
        #     content=self.tr("A control that lets a user pick a date value using a calendar."),
        #     routeKey="dateTimeInterface",
        #     index=0
        # )
        # dateTimeView.addSampleCard(
        #     icon=":/gallery/images/controls/DatePicker.png",
        #     title="DatePicker",
        #     content=self.tr("A control that lets a user pick a date value."),
        #     routeKey="dateTimeInterface",
        #     index=2
        # )
        # dateTimeView.addSampleCard(
        #     icon=":/gallery/images/controls/TimePicker.png",
        #     title="TimePicker",
        #     content=self.tr(
        #         "A configurable control that lets a user pick a time value."),
        #     routeKey="dateTimeInterface",
        #     index=4
        # )
        # self.vBoxLayout.addWidget(dateTimeView)

        # # AI Audio Tools
        # dialogView = SampleCardView(self.tr('AI Audio Tools'), self.view)
        # dialogView.addSampleCard(
        #     icon=":/gallery/images/controls/Flyout.png",
        #     title="Dialog",
        #     content=self.tr("A frameless message dialog."),
        #     routeKey="dialogInterface",
        #     index=0
        # )
        # dialogView.addSampleCard(
        #     icon=":/gallery/images/controls/ContentDialog.png",
        #     title="MessageBox",
        #     content=self.tr("A message dialog with mask."),
        #     routeKey="dialogInterface",
        #     index=1
        # )
        # dialogView.addSampleCard(
        #     icon=":/gallery/images/controls/ColorPicker.png",
        #     title="ColorDialog",
        #     content=self.tr("A dialog that allows user to select color."),
        #     routeKey="dialogInterface",
        #     index=2
        # )
        # dialogView.addSampleCard(
        #     icon=":/gallery/images/controls/Flyout.png",
        #     title="Flyout",
        #     content=self.tr("Shows contextual information and enables user interaction."),
        #     routeKey="dialogInterface",
        #     index=3
        # )
        # dialogView.addSampleCard(
        #     icon=":/gallery/images/controls/TeachingTip.png",
        #     title="TeachingTip",
        #     content=self.tr("A content-rich flyout for guiding users and enabling teaching moments."),
        #     routeKey="dialogInterface",
        #     index=5
        # )
        # self.vBoxLayout.addWidget(dialogView)

        # # AI Chat Tools
        # layoutView = SampleCardView(self.tr('AI Chat Tools'), self.view)
        # layoutView.addSampleCard(
        #     icon=":/gallery/images/controls/Grid.png",
        #     title="FlowLayout",
        #     content=self.tr(
        #         "A layout arranges components in a left-to-right flow, wrapping to the next row when the current row is full."),
        #     routeKey="layoutInterface",
        #     index=0
        # )
        # self.vBoxLayout.addWidget(layoutView)

        # # AI Programming Tools
        # materialView = SampleCardView(self.tr('AI Programming Tools'), self.view)
        # materialView.addSampleCard(
        #     icon=":/gallery/images/controls/Acrylic.png",
        #     title="AcrylicLabel",
        #     content=self.tr(
        #         "A translucent material recommended for panel background."),
        #     routeKey="materialInterface",
        #     index=0
        # )
        # self.vBoxLayout.addWidget(materialView)
        """
        
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

        