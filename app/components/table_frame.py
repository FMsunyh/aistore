
from PyQt5.QtWidgets import QTableWidgetItem
from qfluentwidgets import TableWidget
from qfluentwidgets.components.widgets.line_edit import SearchLineEdit
from app.database.entity.model_info import ModelInfo
from app.common.logger import logger
from app.database.library import Library
from app.common.fuzzy import FuzzyWuzzy

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