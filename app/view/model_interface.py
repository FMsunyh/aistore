'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-10 16:25:44
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-17 14:16:24
FilePath: \aistore\app\view\model_interface.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# coding:utf-8
from pathlib import Path
import subprocess
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy,QTableWidgetItem
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,PushButton,
                            SegmentedToggleToolWidget, FluentIcon,TableWidget)
from qfluentwidgets.components.widgets.line_edit import SearchLineEdit

from app.components.table_frame import TableFrame
from app.database.library import Library
from app.threads.download_thread import DownloadThread

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from app.common.signal_bus import signalBus
from  app.common.config import cfg

class ModelInterface(GalleryInterface):
    """ Navigation view interface """

    def __init__(self, library : Library=None, parent=None):
        t = Translator()
        super().__init__(
            title=t.model,
            subtitle="Model library",
            parent=parent
        )
        self.setObjectName('modelInterface')

        self.library = library

        self.hBoxLayout = QHBoxLayout()

        self.searchLineEdit = SearchLineEdit(self)
        # self.local =  CheckBox(self.tr('local'))
        # self.remove =  CheckBox(self.tr('remove'))
        # self.open_folder = PushButton(self.tr('Open folder'), self, FIF.FOLDER)
        self.refresh_button = PushButton(self.tr('refresh'), self, FIF.SYNC)
        self.refresh_button.setFixedSize(100, 30)
        # self.add_model = PushButton(self.tr('Add model'), self, FIF.ADD)

        self.model_infos =  self.library.model_info_controller.list_all()
        self.table =TableFrame(self.library, self.model_infos, self)

        self.__initWidget()
        self.__connectSignalToSlot()
        
    def __initWidget(self):
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        # self.hBoxLayout.addWidget(self.local)
        # self.hBoxLayout.addWidget(self.remove)
        # self.hBoxLayout.addWidget(self.open_folder)
        self.hBoxLayout.addWidget(self.refresh_button)
        # self.hBoxLayout.addWidget(self.add_model)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)
    
        self.searchLineEdit.setPlaceholderText(self.tr('Search model'))
        self.searchLineEdit.setFixedWidth(300)
        
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.table) 

    def __connectSignalToSlot(self):
        self.searchLineEdit.clearSignal.connect(self.show_condition)
        self.searchLineEdit.searchSignal.connect(self.show_condition)
        self.searchLineEdit.textChanged.connect(self.show_condition)

        signalBus.model_downloadSig.connect(self.download_model)

    def show_condition(self):
        search_text = self.searchLineEdit.text().lower()
        self.show_all()

        if search_text != "":
            self.search(search_text)


    def show_all(self):
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)
            # table.update()        

    def search(self, keyWord: str):
        self.table.search(keyWord)

    def download_model(self, save_folder, url):
        if save_folder == "":
            save_folder = str(Path(cfg.get(cfg.downloadFolder)))

        self.download_thread = DownloadThread(url=url, output_dir=save_folder, creationflags=subprocess.CREATE_NEW_CONSOLE, parent=self)
        # self.download_thread.download_progress.connect(self.progress_window.set_progress)
        # self.download_thread.download_complete.connect(self.on_install_update)
        self.download_thread.start()