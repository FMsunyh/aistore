'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-15 16:38:51
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-18 16:43:39
FilePath: \aistore\app\components\table_frame.py
Description: 
'''

from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget
from qfluentwidgets.components.widgets.line_edit import SearchLineEdit
from app.database.entity.model_info import ModelInfo
from app.common.logger import logger
from app.database.library import Library
from app.common.fuzzy import FuzzyWuzzy
from PyQt5.QtCore import Qt
from qfluentwidgets import PushButton,PrimaryPushButton
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout ,QHeaderView               
from app.common.signal_bus import signalBus
from app.core import wording
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
        self.setHorizontalHeaderLabels([wording.get(f'{label}') for label in self.header_labels])

        self.data = [[str(getattr(instance, attr)) for attr in vars(instance)] for instance in self.model_infos]

        # model_infos = [[str(getattr(instance, attr)) for attr in dir(instance) if not callable(getattr(instance, attr)) and not attr.startswith("__")] for instance in self.model_infos]
        
        for i, model_info in enumerate(self.data):
            for j in range(len(self.header_labels)):
                self.setItem(i, j, QTableWidgetItem(model_info[j]))

        # self.setFixedSize(625, 440)
        self.download_column_index = self.add_download_column()

        self.horizontalHeader().sectionResized.connect(self.update_buttons)

        self.resizeColumnsToContents()

    def __init_fuzzy(self):
        model_names = [instance.name for instance in self.model_infos]
        self.fuzzy.add_keys(model_names)

    def add_download_column(self):
        # Insert new column
        column_index = self.columnCount()
        self.insertColumn(column_index)
        self.setHorizontalHeaderItem(column_index, QTableWidgetItem(self.tr("Download")))

        # Set the minimum width for the download column
        # self.horizontalHeader().setSectionResizeMode(column_index, QHeaderView.Interactive)
        # self.horizontalHeader().setMinimumSectionSize(100)  # Set the minimum width for all columns
        # self.horizontalHeader().resizeSection(column_index, 150)  # Set the initial width for the download column

        # Add download buttons to each row in the new column
        for row in range(self.rowCount()):
            self.add_download_button(row, column_index)

        return column_index

    def add_download_button(self, row, column):
        button =  PrimaryPushButton(self.tr("Download"))
        button.setFixedSize(60, 30)

        button.clicked.connect(lambda: self.download_data(row))

         # Create a QWidget and set QHBoxLayout with alignment to center
        cell_widget = QWidget()
        layout = QHBoxLayout(cell_widget)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(15, 0, 15, 0)  # Optional: remove margins
        cell_widget.setLayout(layout)

        self.setCellWidget(row, column, cell_widget)

    def download_data(self, row):
        def get_cell_text_by_row_label(table, row, label):
            header = table.horizontalHeader()
            for column in range(header.count()):
                if table.horizontalHeaderItem(column).text() == label:
                    item = table.item(row, column)
                    if item:
                        return item.text()
                    break
            return ""

        save_folder = get_cell_text_by_row_label(self, row, 'save_folder')    
        download_url = get_cell_text_by_row_label(self, row, 'download_url')    

        signalBus.model_downloadSig.emit(save_folder, download_url)
        
        print(f"Downloading data for {save_folder}, {download_url}")

    def update_buttons(self):
        # Adjust button positions when the section is resized
        for row in range(self.rowCount()):
            cell_widget = self.cellWidget(row, self.download_column_index)
            if cell_widget:
                cell_widget.setGeometry(self.visualRect(self.model().index(row, self.download_column_index)))

    def search(self, keyWord: str):
        logger.info(f"search model keyWord: {keyWord}")
        matched_indices = self.fuzzy.search(keyWord.lower())
        for row in range(self.rowCount()):
            if row not in matched_indices:
                self.setRowHidden(row, True)