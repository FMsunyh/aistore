'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-11 15:11:16
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-19 15:51:39
FilePath: \aistore\app\view\model_library_interface\sd_model_interface.py
Description: 
'''
# coding:utf-8
import os
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy,QTableWidgetItem,QSpacerItem
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,PushButton,
                            SegmentedToggleToolWidget, FluentIcon,TableWidget)
from qfluentwidgets.components.widgets.line_edit import SearchLineEdit

from app.components.table_frame import TableFrame
from app.database.entity.model_info import ModelInfo
from app.database.entity.model_types import ModelTypes
from app.view.gallery_interface import GalleryInterface
from app.common.translator import Translator
from app.common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF

from app.common.logger import logger
from app.database.library import Library

from app.common.config import cfg

class SDModelInterface(GalleryInterface):
    """ Navigation view interface """

    def __init__(self, library : Library=None, registry=None, parent=None):
        t = Translator()
        super().__init__(
            title=t.model,
            subtitle="Model library",
            parent=parent
        )

        self.library = library
        self.registry = registry
        self.app_card = None

        self.setObjectName('sdModelInterface')

        self.hBoxLayout = QHBoxLayout()

        self.searchLineEdit = SearchLineEdit(self)
        self.local =  CheckBox(self.tr('local'))
        self.remove =  CheckBox(self.tr('remove'))
        self.open_folder_button = PushButton(self.tr('Open folder'), self, FIF.FOLDER)
        self.refresh_button = PushButton(self.tr('Refresh'), self, FIF.SYNC)
        # self.add_model = PushButton(self.tr('Add model'), self, FIF.ADD)

        self.model_types, self.model_infos = self.get_tab_name()
        self.tab_widget = TabInterface(library=library, model_types=self.model_types, model_infos=self.model_infos, parent=self)

        self.__initWidget()
        self.__connectSignalToSlot()
    
    def get_tab_name(self, app_card=None):

        if app_card==None:
            app_id = 1
        else:
            app_id = app_card.app_info.id

        app_models = self.library.app_models_controller.get_models_by_app_id(app_id)

        model_infos =  self.library.model_info_controller.get_model_infos_by_ids([item.model_id for item in app_models])

        model_types = self.library.model_types_controller.get_model_types_by_ids([item.type_id for item in model_infos])

        return model_types, model_infos
    

    def __initWidget(self):
        self.open_folder_button.setFixedSize(150, 30)
        self.refresh_button.setFixedSize(100, 30)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.hBoxLayout.addWidget(self.refresh_button)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hBoxLayout.addItem(spacer)
        
        self.hBoxLayout.addWidget(self.local)
        self.hBoxLayout.addWidget(self.remove)
        self.hBoxLayout.addWidget(self.open_folder_button)
        # self.hBoxLayout.addWidget(self.add_model)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)
    
        self.searchLineEdit.setPlaceholderText(self.tr('Search model'))
        self.searchLineEdit.setFixedWidth(300)
        
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tab_widget) 
        
    def __connectSignalToSlot(self):
        self.searchLineEdit.clearSignal.connect(self.show_condition)
        self.searchLineEdit.searchSignal.connect(self.show_condition)
        self.searchLineEdit.textChanged.connect(self.show_condition)
        self.searchLineEdit.textChanged.connect(self.show_condition)

        self.open_folder_button.clicked.connect(self.open_folder)
        self.refresh_button.clicked.connect(self.refresh)

    def show_condition(self):
        search_text = self.searchLineEdit.text().lower()
        filter_local = self.local.isChecked()
        filter_remove = self.remove.isChecked()

        self.show_all()

        if search_text != "":
            self.search(search_text)

        if filter_local:
            self.filter_local(filter_local)

        if filter_remove:
            self.filter_remove(filter_remove)

    def show_all(self):
        for i in range(self.tab_widget.stackedWidget.count()):
            table = self.tab_widget.stackedWidget.widget(i)
            for row in range(table.rowCount()):
                    table.setRowHidden(row, False)
            # table.update()        

    def search(self, keyWord: str):
        for i in range(self.tab_widget.stackedWidget.count()):
            table = self.tab_widget.stackedWidget.widget(i)
            table.search(keyWord)

    def filter_local(self, is_show: bool):
        # if true, show the local
        pass

    def filter_remove(self, is_show: bool):
        # if true, show the remove
        pass

    def update_window(self, app_card):
        self.app_card = app_card
        self.model_types, self.model_infos = self.get_tab_name(self.app_card)

        # self.tab_widget = TabInterface(library=self.library, model_types=model_types, model_infos=model_infos, parent=self)
        for i in range(self.tab_widget.stackedWidget.count()):
            self.tab_widget.removeTab(0)

        self.tab_widget.update_window(self.model_types, self.model_infos)
        self.toolBar.titleLabel.setText(f"{self.app_card.app_info.title}")

    def open_folder(self):
        logger.info("open folder")
        tab_name = self.tab_widget.tabBar.currentTab().text()

        model_type_id = -1
        for item in self.model_types:
            if item.name == tab_name:
                model_type_id = item.id
                break

        model_folders = self.library.model_folder_controller.get_model_folders_by_app_id(self.app_card.app_info.id)

        directory = ''
        if model_type_id != -1:
            for item in model_folders:
                if item.model_type_id == model_type_id:
                    directory = item.folder
                    break

        if directory != '':
            try:
                directory = f"{cfg.get(cfg.install_folder)}/{self.app_card.app_info.name}/{directory}"
                # os.makedirs(directory)
                os.startfile( directory)
                logger.info(f"Open directory: {directory}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

    def refresh(self):
        # Enable all download buttons
        
        for index in range(self.tab_widget.stackedWidget.count()):
            table_frame = self.tab_widget.stackedWidget.widget(index)
            table_frame.refresh()
            
            # cell_widget = self.table.cellWidget(row, self.download_column_index)
            # if cell_widget:
            #     button = cell_widget.findChild(QPushButton)
            #     if button:
            #         button.setEnabled(True)

        
class TabInterface(QWidget):
    """ Tab interface """

    def __init__(self, library: Library=None, model_types: ModelTypes=None, model_infos: ModelInfo=None, parent=None):
        super().__init__(parent=parent)
        # self.tabCount = 1
        self.library = library
        self.model_types = model_types 

        self.model_infos = model_infos

        self.tabels = []

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.movableCheckBox = CheckBox(self.tr('IsTabMovable'), self)
        self.scrollableCheckBox = CheckBox(self.tr('IsTabScrollable'), self)
        self.shadowEnabledCheckBox = CheckBox(self.tr('IsTabShadowEnabled'), self)
        self.tabMaxWidthLabel = BodyLabel(self.tr('TabMaximumWidth'), self)
        self.tabMaxWidthSpinBox = SpinBox(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.__create_tab(self.model_types, self.model_infos)

        # add items to pivot
        self.__initWidget()


    def __create_tab(self,  model_types, model_infos):
        for model_type in model_types:
            model_infos_with_type = [item for item in model_infos if item.type_id == model_type.id]

            table = TableFrame(self.library, model_infos_with_type, self)
            self.tabels.append(table)
            self.addSubInterface(table, model_type.name, self.tr(f'{model_type.name}'), None)

    def __initWidget(self):
        self.initLayout()

        self.shadowEnabledCheckBox.setChecked(True)

        self.tabMaxWidthSpinBox.setRange(60, 400)
        self.tabMaxWidthSpinBox.setValue(self.tabBar.tabMaximumWidth())

        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)


        self.controlPanel.setObjectName('controlPanel')
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

        if len(self.tabels) > 0:
            qrouter.setDefaultRouteKey(
                self.stackedWidget, self.tabels[0].objectName())

    def connectSignalToSlot(self):
        self.movableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setMovable(self.movableCheckBox.isChecked()))
        self.scrollableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setScrollable(self.scrollableCheckBox.isChecked()))
        self.shadowEnabledCheckBox.stateChanged.connect(
            lambda: self.tabBar.setTabShadowEnabled(self.shadowEnabledCheckBox.isChecked()))

        self.tabMaxWidthSpinBox.valueChanged.connect(self.tabBar.setTabMaximumWidth)

        # self.tabBar.tabAddRequested.connect(self.addTab)
        # self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        # self.tabBar.setTabMaximumWidth(200)

        # self.setFixedHeight(280)
        # self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.movableCheckBox)
        self.panelLayout.addWidget(self.scrollableCheckBox)
        self.panelLayout.addWidget(self.shadowEnabledCheckBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.tabMaxWidthLabel)
        self.panelLayout.addWidget(self.tabMaxWidthSpinBox)

        self.panelLayout.addSpacing(4)

    def addSubInterface(self, widget: TableFrame, objectName, text, icon):
        widget.setObjectName(objectName)
        # widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onDisplayModeChanged(self, index):
        # mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    # def addTab(self):
    #     text = f'硝子酱一级棒卡哇伊×{self.tabCount}'
    #     self.addSubInterface(QLabel('🥰 ' + text), text, text, ':/gallery/images/Smiling_with_heart.png')
    #     self.tabCount += 1

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(TableFrame, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()

    def update_window(self, model_types, model_infos):
        self.__create_tab(model_types, model_infos)
