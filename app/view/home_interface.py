# coding:utf-8
import importlib
from pathlib import Path
import subprocess
import tempfile
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QLabel, QVBoxLayout, QHBoxLayout,QFileDialog

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon,MessageBox,MessageBoxBase,SubtitleLabel,LineEdit,PushButton,CheckBox,StrongBodyLabel,InfoBar, InfoBarIcon, FluentIcon, InfoBarPosition,SearchLineEdit,PrimaryPushButton
import requests

from app.components.app_card import AppCard, AppCardView
from app.core.filesystem import is_directory
from app.core.install_worker import InstallWorker
from app.core.uninstall_worker import UninstallWorker
from app.database.entity.app_versions import AppVersions
from app.database.library import Library
from ..common.config import cfg, HELP_URL, REPO_URL, EXAMPLE_URL, FEEDBACK_URL
from ..common.icon import Icon, FluentIconBase
from ..components.link_card import LinkCardView
from ..components.sample_card import SampleCardView
from ..common.style_sheet import StyleSheet
from ..common.signal_bus import signalBus
from app.common.config import SERVER_IP,SERVER_PORT
import os

from app.common.logger import logger
from app.core import wording
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
            self.tr('Scientific computing, large model training, image rendering.'),
            HELP_URL
        )

        self.linkCardView.addCard(
            ':/gallery/images/h100.png',
            self.tr('GPU Lab'),
            self.tr('GPU rental, GPU computing center.'),
            REPO_URL
        )

        # self.linkCardView.addCard(
        #     FluentIcon.CODE,
        #     self.tr('Code samples'),
        #     self.tr(
        #         'Find samples that demonstrate specific tasks, features and APIs.'),
        #     EXAMPLE_URL
        # )

        # self.linkCardView.addCard(
        #     FluentIcon.FEEDBACK,
        #     self.tr('Send feedback'),
        #     self.tr('Help us improve PyQt-Fluent-Widgets by providing feedback.'),
        #     FEEDBACK_URL
        # )

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

    def __init__(self, library : Library=None, registry=None, parent=None):
        super().__init__(parent=parent)

        self.library = library
        self.registry = registry

        self.install_threads = []
        self.uninstall_threads = []

        self.banner = BannerWidget(self)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.hBoxLayout = QHBoxLayout()
        self.searchLineEdit = SearchLineEdit(self)
        self.installed_checkbox =  CheckBox(self.tr('Installed'))
        
        self.__initWidget()
        self.loadApps3()
        # self.loadSamples()
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

        self.searchLineEdit.setPlaceholderText(self.tr('Search application'))
        self.searchLineEdit.setFixedWidth(300)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.hBoxLayout.addWidget(self.installed_checkbox)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

        self.vBoxLayout.addLayout(self.hBoxLayout)

    def loadApps3(self):
        """ load apps """

        # 1.load types
        # 2.
        # Popular Tools
        self.type_views = []
        index = 0
        for app_type in self.library.app_types:
            type_view = AppCardView(wording.get("app_type."+f'{app_type.name}'), self.view)
            app_infos = self.library.app_info_controller.get_app_infos_by_type_id(app_type.id)
            
            for app_info in app_infos:
                # app_info
                state = 'uninstall'
                for item in self.registry:
                    if item["DisplayName"] == app_info.name:
                        state = 'installed'

                type_view.addAppCard(
                    self.library,
                    app_info,
                    state,
                    routeKey="appInterface",
                    index=index,
                )

                index = index+1

            self.vBoxLayout.addWidget(type_view)
            self.type_views.append(type_view)

    def loadSamples(self):
        """ load samples """
        # basic input samples
        basicInputView = SampleCardView(
            self.tr("Basic input samples"), self.view)
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Button.png",
            title="Button",
            content=self.tr(
                "A control that responds to user input and emit clicked signal."),
            routeKey="basicInputInterface",
            index=0
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Checkbox.png",
            title="CheckBox",
            content=self.tr("A control that a user can select or clear."),
            routeKey="basicInputInterface",
            index=8
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/ComboBox.png",
            title="ComboBox",
            content=self.tr(
                "A drop-down list of items a user can select from."),
            routeKey="basicInputInterface",
            index=10
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/DropDownButton.png",
            title="DropDownButton",
            content=self.tr(
                "A button that displays a flyout of choices when clicked."),
            routeKey="basicInputInterface",
            index=12
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/HyperlinkButton.png",
            title="HyperlinkButton",
            content=self.tr(
                "A button that appears as hyperlink text, and can navigate to a URI or handle a Click event."),
            routeKey="basicInputInterface",
            index=18
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/RadioButton.png",
            title="RadioButton",
            content=self.tr(
                "A control that allows a user to select a single option from a group of options."),
            routeKey="basicInputInterface",
            index=19
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/Slider.png",
            title="Slider",
            content=self.tr(
                "A control that lets the user select from a range of values by moving a Thumb control along a track."),
            routeKey="basicInputInterface",
            index=20
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/SplitButton.png",
            title="SplitButton",
            content=self.tr(
                "A two-part button that displays a flyout when its secondary part is clicked."),
            routeKey="basicInputInterface",
            index=21
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/ToggleSwitch.png",
            title="SwitchButton",
            content=self.tr(
                "A switch that can be toggled between 2 states."),
            routeKey="basicInputInterface",
            index=25
        )
        basicInputView.addSampleCard(
            icon=":/gallery/images/controls/ToggleButton.png",
            title="ToggleButton",
            content=self.tr(
                "A button that can be switched between two states like a CheckBox."),
            routeKey="basicInputInterface",
            index=26
        )
        self.vBoxLayout.addWidget(basicInputView)

        # date time samples
        dateTimeView = SampleCardView(self.tr('Date & time samples'), self.view)
        dateTimeView.addSampleCard(
            icon=":/gallery/images/controls/CalendarDatePicker.png",
            title="CalendarPicker",
            content=self.tr("A control that lets a user pick a date value using a calendar."),
            routeKey="dateTimeInterface",
            index=0
        )
        dateTimeView.addSampleCard(
            icon=":/gallery/images/controls/DatePicker.png",
            title="DatePicker",
            content=self.tr("A control that lets a user pick a date value."),
            routeKey="dateTimeInterface",
            index=2
        )
        dateTimeView.addSampleCard(
            icon=":/gallery/images/controls/TimePicker.png",
            title="TimePicker",
            content=self.tr(
                "A configurable control that lets a user pick a time value."),
            routeKey="dateTimeInterface",
            index=4
        )
        self.vBoxLayout.addWidget(dateTimeView)

        # dialog samples
        dialogView = SampleCardView(self.tr('Dialog samples'), self.view)
        dialogView.addSampleCard(
            icon=":/gallery/images/controls/Flyout.png",
            title="Dialog",
            content=self.tr("A frameless message dialog."),
            routeKey="dialogInterface",
            index=0
        )
        dialogView.addSampleCard(
            icon=":/gallery/images/controls/ContentDialog.png",
            title="MessageBox",
            content=self.tr("A message dialog with mask."),
            routeKey="dialogInterface",
            index=1
        )
        dialogView.addSampleCard(
            icon=":/gallery/images/controls/ColorPicker.png",
            title="ColorDialog",
            content=self.tr("A dialog that allows user to select color."),
            routeKey="dialogInterface",
            index=2
        )
        dialogView.addSampleCard(
            icon=":/gallery/images/controls/Flyout.png",
            title="Flyout",
            content=self.tr("Shows contextual information and enables user interaction."),
            routeKey="dialogInterface",
            index=3
        )
        dialogView.addSampleCard(
            icon=":/gallery/images/controls/TeachingTip.png",
            title="TeachingTip",
            content=self.tr("A content-rich flyout for guiding users and enabling teaching moments."),
            routeKey="dialogInterface",
            index=5
        )
        self.vBoxLayout.addWidget(dialogView)

        # layout samples
        layoutView = SampleCardView(self.tr('Layout samples'), self.view)
        layoutView.addSampleCard(
            icon=":/gallery/images/controls/Grid.png",
            title="FlowLayout",
            content=self.tr(
                "A layout arranges components in a left-to-right flow, wrapping to the next row when the current row is full."),
            routeKey="layoutInterface",
            index=0
        )
        self.vBoxLayout.addWidget(layoutView)

        # material samples
        materialView = SampleCardView(self.tr('Material samples'), self.view)
        materialView.addSampleCard(
            icon=":/gallery/images/controls/Acrylic.png",
            title="AcrylicLabel",
            content=self.tr(
                "A translucent material recommended for panel background."),
            routeKey="materialInterface",
            index=0
        )
        self.vBoxLayout.addWidget(materialView)

        # menu samples
        menuView = SampleCardView(self.tr('Menu & toolbars samples'), self.view)
        menuView.addSampleCard(
            icon=":/gallery/images/controls/MenuFlyout.png",
            title="RoundMenu",
            content=self.tr(
                "Shows a contextual list of simple commands or options."),
            routeKey="menuInterface",
            index=0
        )
        menuView.addSampleCard(
            icon=":/gallery/images/controls/CommandBar.png",
            title="CommandBar",
            content=self.tr(
                "Shows a contextual list of simple commands or options."),
            routeKey="menuInterface",
            index=2
        )
        menuView.addSampleCard(
            icon=":/gallery/images/controls/CommandBarFlyout.png",
            title="CommandBarFlyout",
            content=self.tr(
                "A mini-toolbar displaying proactive commands, and an optional menu of commands."),
            routeKey="menuInterface",
            index=3
        )
        self.vBoxLayout.addWidget(menuView)

        # navigation
        navigationView = SampleCardView(self.tr('Navigation'), self.view)
        navigationView.addSampleCard(
            icon=":/gallery/images/controls/BreadcrumbBar.png",
            title="BreadcrumbBar",
            content=self.tr(
                "Shows the trail of navigation taken to the current location."),
            routeKey="navigationViewInterface",
            index=0
        )
        navigationView.addSampleCard(
            icon=":/gallery/images/controls/Pivot.png",
            title="Pivot",
            content=self.tr(
                "Presents information from different sources in a tabbed view."),
            routeKey="navigationViewInterface",
            index=1
        )
        navigationView.addSampleCard(
            icon=":/gallery/images/controls/TabView.png",
            title="TabView",
            content=self.tr(
                "Presents information from different sources in a tabbed view."),
            routeKey="navigationViewInterface",
            index=3
        )
        self.vBoxLayout.addWidget(navigationView)

        # scroll samples
        scrollView = SampleCardView(self.tr('Scrolling samples'), self.view)
        scrollView.addSampleCard(
            icon=":/gallery/images/controls/ScrollViewer.png",
            title="ScrollArea",
            content=self.tr(
                "A container control that lets the user pan and zoom its content smoothly."),
            routeKey="scrollInterface",
            index=0
        )
        scrollView.addSampleCard(
            icon=":/gallery/images/controls/PipsPager.png",
            title="PipsPager",
            content=self.tr(
                "A control to let the user navigate through a paginated collection when the page numbers do not need to be visually known."),
            routeKey="scrollInterface",
            index=3
        )
        self.vBoxLayout.addWidget(scrollView)

        # state info samples
        stateInfoView = SampleCardView(self.tr('Status & info samples'), self.view)
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/ProgressRing.png",
            title="StateToolTip",
            content=self.tr(
                "Shows the apps progress on a task, or that the app is performing ongoing work that does block user interaction."),
            routeKey="statusInfoInterface",
            index=0
        )
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/InfoBadge.png",
            title="InfoBadge",
            content=self.tr(
                "An non-intrusive Ul to display notifications or bring focus to an area."),
            routeKey="statusInfoInterface",
            index=3
        )
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/InfoBar.png",
            title="InfoBar",
            content=self.tr(
                "An inline message to display app-wide status change information."),
            routeKey="statusInfoInterface",
            index=4
        )
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/ProgressBar.png",
            title="ProgressBar",
            content=self.tr(
                "Shows the apps progress on a task, or that the app is performing ongoing work that doesn't block user interaction."),
            routeKey="statusInfoInterface",
            index=8
        )
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/ProgressRing.png",
            title="ProgressRing",
            content=self.tr(
                "Shows the apps progress on a task, or that the app is performing ongoing work that doesn't block user interaction."),
            routeKey="statusInfoInterface",
            index=10
        )
        stateInfoView.addSampleCard(
            icon=":/gallery/images/controls/ToolTip.png",
            title="ToolTip",
            content=self.tr(
                "Displays information for an element in a pop-up window."),
            routeKey="statusInfoInterface",
            index=1
        )
        self.vBoxLayout.addWidget(stateInfoView)

        # text samples
        textView = SampleCardView(self.tr('Text samples'), self.view)
        textView.addSampleCard(
            icon=":/gallery/images/controls/TextBox.png",
            title="LineEdit",
            content=self.tr("A single-line plain text field."),
            routeKey="textInterface",
            index=0
        )
        textView.addSampleCard(
            icon=":/gallery/images/controls/PasswordBox.png",
            title="PasswordLineEdit",
            content=self.tr("A control for entering passwords."),
            routeKey="textInterface",
            index=2
        )
        textView.addSampleCard(
            icon=":/gallery/images/controls/NumberBox.png",
            title="SpinBox",
            content=self.tr(
                "A text control used for numeric input and evaluation of algebraic equations."),
            routeKey="textInterface",
            index=3
        )
        textView.addSampleCard(
            icon=":/gallery/images/controls/RichEditBox.png",
            title="TextEdit",
            content=self.tr(
                "A rich text editing control that supports formatted text, hyperlinks, and other rich content."),
            routeKey="textInterface",
            index=8
        )
        self.vBoxLayout.addWidget(textView)

        # view samples
        collectionView = SampleCardView(self.tr('View samples'), self.view)
        collectionView.addSampleCard(
            icon=":/gallery/images/controls/ListView.png",
            title="ListView",
            content=self.tr(
                "A control that presents a collection of items in a vertical list."),
            routeKey="viewInterface",
            index=0
        )
        collectionView.addSampleCard(
            icon=":/gallery/images/controls/DataGrid.png",
            title="TableView",
            content=self.tr(
                "The DataGrid control provides a flexible way to display a collection of data in rows and columns."),
            routeKey="viewInterface",
            index=1
        )
        collectionView.addSampleCard(
            icon=":/gallery/images/controls/TreeView.png",
            title="TreeView",
            content=self.tr(
                "The TreeView control is a hierarchical list pattern with expanding and collapsing nodes that contain nested items."),
            routeKey="viewInterface",
            index=2
        )
        collectionView.addSampleCard(
            icon=":/gallery/images/controls/FlipView.png",
            title="FlipView",
            content=self.tr(
                "Presents a collection of items that the user can flip through,one item at a time."),
            routeKey="viewInterface",
            index=4
        )
        self.vBoxLayout.addWidget(collectionView)

    def set_registry(self, registry):
        self.registry = registry

    def _aboutCardClick(self):
        print("__connectSignalToSlot")

    def __connectSignalToSlot(self):
        signalBus.software_installSig.connect(self.software_install)
        signalBus.software_uninstallSig.connect(self.software_uninstall)
        signalBus.software_runSig.connect(self.software_run)
        signalBus.software_stopSig.connect(self.software_stop)
        self.searchLineEdit.clearSignal.connect(self.show_condition)
        self.searchLineEdit.searchSignal.connect(self.show_condition)
        self.searchLineEdit.textChanged.connect(self.show_condition)
        self.installed_checkbox.stateChanged.connect(self.show_condition)

    def software_run(self, app_card):
        app_name = app_card.app_info.name
        logger.info(f"Run the process: {app_name}")

        # print(app_card.app_info.name)

        # title = self.tr('Run ' + app_card.app_info.name)
        # content = self.tr(f"Run on desktop shortcut")
        # w = MessageBox(title, content, self)

        # if w.exec():
        #     print("run")

        command = f"{cfg.get(cfg.install_folder)}/{app_name}/launch.bat"
        # command = "echo Hello, World!"
        start_directory = f"{cfg.get(cfg.install_folder)}/{app_name}"
        try:
            # app_card.process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=start_directory, encoding='utf-8', creationflags=subprocess.CREATE_NEW_CONSOLE)
            app_card.process = subprocess.Popen(command,  text=True, cwd=start_directory, creationflags=subprocess.CREATE_NEW_CONSOLE, encoding='utf-8')

            logger.info(f'Run {command}, pid: {app_card.process.pid}')
            # logger.info(f'output, return: {output}')
            # logger.info(f'error, return: {error}')
        except subprocess.CalledProcessError as e:
            logger.error(f'Command failed with exit status {e.returncode}')
            logger.error(f'Stdout: {e.stdout}')
            logger.error(f'Stderr: {e.stderr}')
        except FileNotFoundError as e:
            logger.error(f'Command not found: {e}')
        except subprocess.TimeoutExpired as e:
            logger.error(f'Command timed out: {e}')
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
               
        app_card.set_state('running')
        app_card.refreshSig.emit()

        InfoBar.success(
            title=self.tr(f'Running {app_card.app_info.title}'),
            content=self.tr("It takes some time to start the application, please be patient and wait for a moment."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self.window()
        )

        logger.info("Done")


    def software_stop(self, app_card):
        if app_card.process is None:
            return
        
        app_name = app_card.app_info.name
        logger.info(f"Close the process: {app_name}")

        # app_card.process.terminate()
        # app_card.process.kill()

        command= "taskkill /F /T /PID " + str(app_card.process.pid)

        try:
            result = subprocess.run(command, shell=True)
            logger.info(f'Run {command}, return: {result}')
        except subprocess.CalledProcessError as e:
            logger.error(f'Command failed with exit status {e.returncode}')
            logger.error(f'Stdout: {e.stdout}')
            logger.error(f'Stderr: {e.stderr}')
        except FileNotFoundError as e:
            logger.error(f'Command not found: {e}')
        except subprocess.TimeoutExpired as e:
            logger.error(f'Command timed out: {e}')
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')


        # app_card.process.wait()
        app_card.set_state('stop')
        app_card.refreshSig.emit()

        InfoBar.success(
            title=self.tr(f'Stopping {app_card.app_info.title}'),
            content=self.tr("It takes some time to stop the application, please be patient and wait for a moment."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self.window()
        )

        logger.info("Done")


    def software_install(self, app_card: AppCard, app_version: AppVersions):
        app_name = app_card.app_info.name
        app_title = app_card.app_info.title
        # logger.info(app_card.app_info.name)

        title = self.tr('Install ') + f"{app_title}"
        w = CustomMessageBox(title=title, app_name=app_name, parent=self.window())
        if w.exec():
            logger.info("Start to install {}".format(app_title))

            url = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/{app_name}/{app_name}-{app_version.version_number}.zip"
            logger.info(f"{url}, {app_version.version_number}")

            # temp_directory_path = os.path.join(tempfile.gettempdir(), 'aistore', app_name)
            temp_directory_path = f"{cfg.get(cfg.downloadFolder)}/{app_name}"
            Path(temp_directory_path).mkdir(parents = True, exist_ok = True)
            logger.info(f"download folder:{temp_directory_path}")

            thread = InstallWorker(app_name, app_version.version_number, temp_directory_path, url,  cfg.get(cfg.install_folder))
            thread.download_progress.connect(app_card.update_progress_bar)
            # thread.download_completed.connect(self.update_completed)
            thread.unzip_progress.connect(app_card.update_progress_bar)
            # thread.unzip_completed.connect(self.update_unzip_status)
            # thread.completed.connect(self.update_unzip_status)
            
            thread.finished.connect(lambda t=thread, app_card=app_card: self.on_install_thread_finished(t, app_card))
            thread.error_occurred.connect(lambda message, t=thread, app_card=app_card: self.on_install_thread_error(message, t, app_card))

            self.install_threads.append(thread)
            thread.start()

            app_card.set_state('installing')
            app_card.refreshSig.emit()
            logger.info("Finished")

    def software_uninstall(self, app_card: AppCard):
        app_name = app_card.app_info.name
        app_title = app_card.app_info.title

        title = self.tr('Uninstall')
        content = self.tr("Do you want to uninstall ") + f"{app_title} ?"
        w = MessageBox(title, content, self.window())

        if w.exec():
            logger.info("Start to uninstall {}".format(app_title))

            thread = UninstallWorker(app_name , cfg.get(cfg.install_folder))
            thread.progress.connect(app_card.update_progress_bar)
            # thread.completed.connect(self.update_completed)
            thread.finished.connect(lambda t=thread, app_card=app_card: self.on_uninstall_thread_finished(t, app_card))
            self.uninstall_threads.append(thread)
            thread.start()
            app_card.set_state('uninstalling')
            app_card.refreshSig.emit()
            logger.info("Finished")


    def on_install_thread_finished(self, thread, app_card: AppCard):
        if not thread in self.install_threads:
            return
        
        app_name = app_card.app_info.name
        app_title = app_card.app_info.title

        self.install_threads.remove(thread)

        app_card.set_state('install_completed')
        app_card.refreshSig.emit()

        title = self.tr('Successful installation ') + f"{app_title}"
        content = self.tr(f"Do you want to run ") + f"{app_title}?"
        w = MessageBox(title, content, self.window())
        if w.exec():
            # title = self.tr('Run ' + app_card.app_info.name)
            # content = self.tr(f"Run on desktop shortcut")
            # w = MessageBox(title, content, self)

            # if w.exec():
            #     print("run")
       
            self.software_run(app_card)

    def on_install_thread_error(self, error_message, thread, app_card: AppCard):
        app_name = app_card.app_info.name
        app_title = app_card.app_info.title
        
        self.install_threads.remove(thread)
        thread.quit()
        # thread = None

        app_card.set_state('uninstall')
        app_card.refreshSig.emit()

        title = self.tr('Install Error')
        content = f"{app_title}: " + f"{error_message}"

        w = MessageBox(title, content, self.window())
        w.hideCancelButton()
        w.exec()    


    def on_uninstall_thread_finished(self, thread, app_card):
        app_name = app_card.app_info.name

        for item in self.registry:
            if item["DisplayName"] == app_name:
                self.registry.remove(item)
        self.uninstall_threads.remove(thread)

        app_card.set_state('uninstall_completed')
        app_card.refreshSig.emit()


    def show_condition(self):
        search_text = self.searchLineEdit.text().lower()
        filter_installed = self.installed_checkbox.isChecked()

        self.showAllApps()

        if search_text != "":
            self.search(search_text)

        if filter_installed:
            self.filter_installed(filter_installed)

    def showAllApps(self):
        logger.info("show all appps")
        for type_view in self.type_views:
            type_view.showAllApps()

    def search(self, keyWord: str):
        for type_view in self.type_views:
            type_view.search(keyWord)

    def filter_installed(self, installed_checkbox: bool):
        for type_view in self.type_views:
            type_view.filter_installed(installed_checkbox)

    # def paintEvent(self, e):
    #     # super().paintEvent(e)
    #     # # self.banner.paintEvent(e)
    #     # self.show_condition()
    #     self.view.update()
        
class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, title, app_name, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr(title), self)
        self.app_name = app_name
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        # change the text of button
        self.yesButton.setText(self.tr('Install'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(500)
        # self.yesButton.setDisabled(True)

                # 安装路径部分
        path_layout = QHBoxLayout()
        self.path_label = StrongBodyLabel(self.tr('Select Installation Path:'))
        path_layout.addWidget(self.path_label)
        self.path_edit = LineEdit(self)
        # self.path_edit.setPlaceholderText(self.tr('Enter installation path'))
        defualt_path = os.path.join(r"D:\aistore", self.app_name)
                                    
        self.path_edit.setText(defualt_path)
        # self.path_edit.setClearButtonEnabled(True)
        self.path_edit.setDisabled(True)

        path_layout.addWidget(self.path_edit)
        self.browse_button = PushButton(self.tr('Browse'))
        self.browse_button.clicked.connect(self.browse)
        # path_layout.addWidget(self.browse_button)
        self.viewLayout.addLayout(path_layout)

        # 创建桌面快捷方式复选框
        self.shortcut_checkbox = CheckBox(self.tr('Create Desktop Shortcut'))
        self.shortcut_checkbox.setChecked(True)
        self.shortcut_checkbox.setDisabled(True)
        self.viewLayout.addWidget(self.shortcut_checkbox)


        # self.path_edit.textChanged.connect(self._validateUrl)
        # self.yesButton.setDisabled(True)

    # def _validateUrl(self, text):
    #     self.yesButton.setEnabled(is_directory(text))

    def browse(self):
        # 打开文件夹选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self, "Select Installation Path", "", options=options)
        if directory:
            self.path_edit.setText(directory)
  