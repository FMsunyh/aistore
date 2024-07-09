# coding:utf-8
import importlib
from pathlib import Path
import subprocess
import tempfile
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QBrush, QPainterPath, QLinearGradient
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QLabel, QVBoxLayout, QHBoxLayout,QFileDialog

from qfluentwidgets import ScrollArea, isDarkTheme, FluentIcon,MessageBox,MessageBoxBase,SubtitleLabel,LineEdit,PushButton,CheckBox,StrongBodyLabel,InfoBar, InfoBarIcon, FluentIcon, InfoBarPosition
import requests

from app.components.app_card import AppCard, AppCardView
from app.core.filesystem import is_directory
from app.core.install_worker import InstallWorker
from app.core.uninstall_worker import UninstallWorker
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

        self.__initWidget()
        self.loadApps3()
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

    def loadApps3(self):
        """ load apps """

        # 1.load types
        # 2.
        # Popular Tools
        self.type_views = []
        for app_type in self.library.app_types:

            type_view = AppCardView(self.tr(f'{app_type.name}'), self.view)

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
                    routeKey="navigationViewInterface",
                    index=0,
                )

            self.vBoxLayout.addWidget(type_view)
            self.type_views.append(type_view)


    def loadApps2(self):
        """ load apps """

        # Popular Tools
        self.popularView = AppCardView(self.tr('Popular Tools'), self.view)

        for item in self.library.app_infos:
            name = item.name
            icon = item.icon
            title = item.title
            content = item.description

            # app_info, 
            self.popularView.addAppCard(
                name=name,
                icon=icon,
                title=title,
                content=self.tr(content),
                routeKey="navigationViewInterface",
                index=0,
                
            )

        self.vBoxLayout.addWidget(self.popularView)

    def loadApps(self):
        """ load apps """

        # Popular Tools
        self.popularView = AppCardView(self.tr('Popular Tools'), self.view)
        self.popularView.addAppCard(
            icon=":/gallery/images/controls/CommandBarFlyout.png",
            title="Stable Diffusion WebUI",
            content=self.tr("A web interface for Stable Diffusion WebUI."),
            routeKey="navigationViewInterface",
            index=0,
            name="sd_webui"
        )

        self.popularView.addAppCard(
            icon=":/gallery/images/controls/CommandBar.png",
            title="Kohya_ss GUI",
            content=self.tr("A web interface for training stable diffusion model, base model or lora."),
            routeKey="navigationViewInterface",
            index=0,
            name="kohya_ss"
        )

        self.popularView.addAppCard(
            icon=":/gallery/images/controls/MenuFlyout.png",
            title="FaceFusion",
            content=self.tr("A web interface for FaceFusion."),
            routeKey="navigationViewInterface",
            index=0,
            name="facefusion"
        )
        
        self.vBoxLayout.addWidget(self.popularView)

    def set_registry(self, registry):
        self.registry = registry


    def _aboutCardClick(self):
        print("__connectSignalToSlot")

    def __connectSignalToSlot(self):
        signalBus.software_installSig.connect(self.software_install)
        signalBus.software_uninstallSig.connect(self.software_uninstall)
        signalBus.software_runSig.connect(self.software_run)
        signalBus.software_stopSig.connect(self.software_stop)

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


    def software_install(self, app_card: AppCard):
        def get_url(app_name):
            info_url = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/{app_name}/info.txt"
            response = requests.get(info_url)
            version = ""
            if response.status_code == 200:
                app_info = response.json()
                version = app_info['version']
                filename = app_info['filename']

            url = f"http://{SERVER_IP}:{SERVER_PORT}/chfs/shared/{app_name}/{filename}"

            return url, version

        app_name = app_card.app_info.name
        app_title = app_card.app_info.title
        # logger.info(app_card.app_info.name)

        title = self.tr('Install ') + f"{app_title}"
        w = CustomMessageBox(title=title, app_name=app_name, parent=self.window())
        if w.exec():
            logger.info("Start to install {}".format(app_title))

            url, version = get_url(app_name)
            logger.info(f"{url}, {version}")

            temp_directory_path = os.path.join(tempfile.gettempdir(), 'aistore', app_name)
            Path(temp_directory_path).mkdir(parents = True, exist_ok = True)
            logger.info(f"download folder:{temp_directory_path}")

            thread = InstallWorker(app_name, version, temp_directory_path, url,  cfg.get(cfg.install_folder))
            thread.download_progress.connect(app_card.update_progress_bar)
            # thread.download_completed.connect(self.update_completed)
            thread.unzip_progress.connect(app_card.update_progress_bar)
            # thread.unzip_completed.connect(self.update_unzip_status)
            # thread.completed.connect(self.update_unzip_status)
            
            thread.finished.connect(lambda t=thread, app_card=app_card: self.on_install_thread_finished(t, app_card))
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


    def on_uninstall_thread_finished(self, thread, app_card):
        app_name = app_card.app_info.name

        for item in self.registry:
            if item["DisplayName"] == app_name:
                self.registry.remove(item)
        self.uninstall_threads.remove(thread)

        app_card.set_state('uninstall_completed')
        app_card.refreshSig.emit()

    # def refresh(self):
    #     for view in self.type_views:
    #         view.refresh()
        

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
  