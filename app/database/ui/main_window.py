# ui/main_window.py
import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from app.database.controller.user_controller import UserController
from app.database.controller.app_info_controller import AppInfoController
from app.database.dao.user_dao import UserDao
from app.database.dao.app_info_dao import AppInfoDao
from app.database.service.user_service import UserService
from app.database.service.app_info_service import AppInfoService
from app.database.entity.user import User
from app.database.db_initializer import DBInitializer
from PyQt5.QtSql import QSqlDatabase

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # app_info_dao = AppInfoDao('db.sqlite')
        # app_info_service = AppInfoService(app_info_dao)
        # self.app_info_controller = AppInfoController(app_info_service)

        DBInitializer.init()
        self.app_info_controller = AppInfoController(QSqlDatabase.database(DBInitializer.CONNECTION_NAME))

        self.initUI()

    def initUI(self):
        self.setWindowTitle("App Info Management System")

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.iconInput = QLineEdit(self)
        self.iconInput.setPlaceholderText("Icon")
        self.layout.addWidget(self.iconInput)

        self.nameInput = QLineEdit(self)
        self.nameInput.setPlaceholderText("Name")
        self.layout.addWidget(self.nameInput)

        self.contentInput = QLineEdit(self)
        self.contentInput.setPlaceholderText("Content")
        self.layout.addWidget(self.contentInput)

        self.addButton = QPushButton("Add App Info", self)
        self.addButton.clicked.connect(self.addAppInfo)
        self.layout.addWidget(self.addButton)

        self.updateButton = QPushButton("Update App Info", self)
        self.updateButton.clicked.connect(self.updateAppInfo)
        self.layout.addWidget(self.updateButton)

        self.deleteButton = QPushButton("Delete App Info", self)
        self.deleteButton.clicked.connect(self.deleteAppInfo)
        self.layout.addWidget(self.deleteButton)

        self.appInfoList = QListWidget(self)
        self.layout.addWidget(self.appInfoList)

        self.refreshAppInfoList()

    def addAppInfo(self):
        icon = self.iconInput.text()
        name = self.nameInput.text()
        content = self.contentInput.text()
        if icon and name and content:
            self.app_info_controller.add_app_info(icon, name, content)
            self.refreshAppInfoList()
        else:
            QMessageBox.warning(self, "Input Error", "Icon, Name, and Content cannot be empty")

    def updateAppInfo(self):
        selected_item = self.appInfoList.currentItem()
        if selected_item:
            app_id = selected_item.data(1)
            icon = self.iconInput.text()
            name = self.nameInput.text()
            content = self.contentInput.text()
            if icon and name and content:
                self.app_info_controller.update_app_info(app_id, icon, name, content)
                self.refreshAppInfoList()
            else:
                QMessageBox.warning(self, "Input Error", "Icon, Name, and Content cannot be empty")
        else:
            QMessageBox.warning(self, "Selection Error", "No app info selected")

    def deleteAppInfo(self):
        selected_item = self.appInfoList.currentItem()
        if selected_item:
            app_id = selected_item.data(1)
            self.app_info_controller.delete_app_info(app_id)
            self.refreshAppInfoList()
        else:
            QMessageBox.warning(self, "Selection Error", "No app info selected")

    def refreshAppInfoList(self):
        self.appInfoList.clear()
        app_infos = self.app_info_controller.get_all_app_info()
        for app_info in app_infos:
            item = QListWidgetItem(str(app_info))
            item.setData(1, app_info.app_id)
            self.appInfoList.addItem(item)
