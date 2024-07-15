# coding:utf-8
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy,QTableWidgetItem
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,PushButton,
                            SegmentedToggleToolWidget, FluentIcon,TableWidget)
from qfluentwidgets.components.widgets.line_edit import SearchLineEdit

from app.common.fuzzy import FuzzyWuzzy
from app.database.entity.model_info import ModelInfo
from app.database.entity.model_types import ModelTypes
from app.view.gallery_interface import GalleryInterface
from app.common.translator import Translator
from app.common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF

from app.common.logger import logger
from app.database.library import Library

class SDModelInterface(GalleryInterface):
    """ Navigation view interface """

    def __init__(self, library : Library=None, registry=None, parent=None):
        t = Translator()
        super().__init__(
            title=t.model,
            subtitle="SD Model library",
            parent=parent
        )

        self.library = library
        self.registry = registry


        self.setObjectName('sdModelInterface')

        self.hBoxLayout = QHBoxLayout()

        self.searchLineEdit = SearchLineEdit(self)
        self.local =  CheckBox(self.tr('local'))
        self.remove =  CheckBox(self.tr('remove'))
        self.open_folder = PushButton(self.tr('Open folder'), self, FIF.FOLDER)
        self.refresh = PushButton(self.tr('Refresh'), self, FIF.SYNC)
        self.add_model = PushButton(self.tr('Add model'), self, FIF.ADD)

        model_types, model_infos = self.get_tab_name()
        self.tab_widget = TabInterface(library=library, model_types=model_types, model_infos=model_infos, parent=self)

        self.__initWidget()
        self.__connectSignalToSlot()
    
    def get_tab_name(self):
        app_models = self.library.app_models_controller.get_models_by_app_id(1)
        model_types = self.library.model_types_controller.get_model_types_by_ids([item.id for item in app_models])

        model_infos =  self.library.model_info_controller.get_model_infos_by_ids([item.model_id for item in app_models])

        return model_types, model_infos
    

    def __initWidget(self):
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.hBoxLayout.addWidget(self.local)
        self.hBoxLayout.addWidget(self.remove)
        self.hBoxLayout.addWidget(self.open_folder)
        self.hBoxLayout.addWidget(self.refresh)
        self.hBoxLayout.addWidget(self.add_model)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)
    
        self.searchLineEdit.setPlaceholderText(self.tr('Search model'))
        self.searchLineEdit.setFixedWidth(300)
        
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.tab_widget) 
        
    def __connectSignalToSlot(self):
        self.searchLineEdit.clearSignal.connect(self.show_condition)
        self.searchLineEdit.searchSignal.connect(self.show_condition)
        self.searchLineEdit.textChanged.connect(self.show_condition)

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


    # def show_all(self):
    #     for i in range(self.tab_widget.stackedWidget.count()):
    #         table = self.tab_widget.stackedWidget.widget(i)
    #         for row in range(table.rowCount()):
    #             match = False
    #             for col in range(table.columnCount()):
    #                 item = table.item(row, col)
    #                 # if search_term in item.text().lower():
    #                 import random
    #                 if random.randint(1,10) < 5:
    #                     match = True
    #                     break
    #             table.setRowHidden(row, not match)

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

    def update_window(self):
        pass

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

        self.create_tab(self.library, self.model_types, self.model_infos)

        # add items to pivot
        self.__initWidget()


    def create_tab(self, library, model_types, model_infos):
        for model_type in model_types:
            model_infos_with_type = [item for item in model_infos if item.type_id == model_type.id]

            table = TableFrame(library, model_infos_with_type, self)
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

    def addSubInterface(self, widget: QLabel, objectName, text, icon):
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

    # def removeTab(self, index):
    #     item = self.tabBar.tabItem(index)
    #     widget = self.findChild(QLabel, item.routeKey())

    #     self.stackedWidget.removeWidget(widget)
    #     self.tabBar.removeTab(index)
    #     widget.deleteLater()

class TableFrame(TableWidget):

    def __init__(self, library: Library=None, model_infos: ModelInfo=None, parent=None):
        super().__init__(parent)
        self.library = library
        self.model_infos = model_infos

        # import copy
        # self.model_infos = [copy.deepcopy(model_infos[0]) for _ in range(100)] 
        # for i in range(len(self.model_infos)):
        #     self.model_infos[i].id = i+1
        
        self.header_labels = []
        self.data = [[]]
        self.fuzzy = FuzzyWuzzy()

        self.__init_table()
        self.__init_fuzzy()

    def __init_table(self):
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)
    
        self.header_labels = self.library.model_info_controller.get_fields()
        self.setColumnCount(len(self.header_labels))

        self.setRowCount(len(self.model_infos))
        self.setHorizontalHeaderLabels([self.tr(f'{label}') for label in self.header_labels])

        self.data = [[str(getattr(instance, attr)) for attr in vars(instance)] for instance in self.model_infos]

        # model_infos = [[str(getattr(instance, attr)) for attr in dir(instance) if not callable(getattr(instance, attr)) and not attr.startswith("__")] for instance in self.model_infos]
        
        for i, model_info in enumerate(self.data):
            for j in range(len(self.header_labels)):
                self.setItem(i, j, QTableWidgetItem(model_info[j]))

        # self.setFixedSize(625, 440)
        self.resizeColumnsToContents()

    def __init_fuzzy(self):
        model_names = [instance.name for instance in self.model_infos]
        self.fuzzy.add_keys(model_names)

    def search(self, keyWord: str):
        logger.info(f"search model keyWord: {keyWord}")
        matched_indices = self.fuzzy.search(keyWord.lower())
        for row in range(self.rowCount()):
            if row not in matched_indices:
                self.setRowHidden(row, True)