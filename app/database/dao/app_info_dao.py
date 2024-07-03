from app.database.dao.dao_base import DaoBase
from app.database.entity.app_info import AppInfo

class AppInfoDao(DaoBase):
    table = 'tbl_app_info'
    fields = ['id', 'icon', 'name', 'title', 'brief_introduction','description', 'type_id','developer_id','release_date']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                icon TEXT NOT NULL,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                brief_introduction TEXT NOT NULL,
                description TEXT NOT NULL,
                type_id INTEGER,
                developer_id INTEGER,
                release_date TEXT,
                FOREIGN  KEY (type_id) REFERENCES tbl_app_Types(id),
                FOREIGN  KEY (developer_id) REFERENCES tbl_developers(id)
            )
        """)
        return success