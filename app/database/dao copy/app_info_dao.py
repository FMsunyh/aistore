from app.database.dao.dao_base import DaoBase
from app.database.entity.app_info import AppInfo

class AppInfoDao(DaoBase):
    table = 'tbl_app_info'
    fields = ['id', 'icon', 'name', 'content']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                icon TEXT NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        return success
    
    def add_app_info(self, app_info):
        # query = self.query
        # query.prepare(f"INSERT INTO {self.table} (id, icon, name, content) VALUES (?, ?, ?, ?)")
        # query.addBindValue(app_info.app_id)
        # query.addBindValue(app_info.icon)
        # query.addBindValue(app_info.name)
        # query.addBindValue(app_info.content)
        # query.exec_()

        self.insert(app_info)

    def update_app_info(self, app_info):
        query = self.query
        query.prepare(f"UPDATE {self.table} SET icon = ?, name = ?, content = ? WHERE id = ?")
        query.addBindValue(app_info.icon)
        query.addBindValue(app_info.name)
        query.addBindValue(app_info.content)
        query.addBindValue(app_info.app_id)
        query.exec_()

    def delete_app_info(self, app_id):
        query = self.query
        query.prepare(f"DELETE FROM {self.table} WHERE id = ?")
        query.addBindValue(app_id)
        query.exec_()

    def get_app_info_by_id(self, app_id):
        query = self.query
        query.prepare(f"SELECT id, icon, name, content FROM {self.table} WHERE id = ?")
        query.addBindValue(app_id)
        query.exec_()
        if query.next():
            return AppInfo(query.value(0), query.value(1), query.value(2), query.value(3))
        return None

    # def get_all_app_info(self):
    #     query = self.query
    #     query.exec_(f"SELECT id, icon, name, content FROM {self.table}")
    #     app_infos = []
    #     while query.next():
    #         app_infos.append(AppInfo(query.value(0), query.value(1), query.value(2), query.value(3)))
    #     return app_infos
    
    def get_all_app_info(self):
        app_infos = self.listAll()
        return app_infos