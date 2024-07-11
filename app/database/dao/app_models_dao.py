from app.database.dao.dao_base import DaoBase

class AppModelsDao(DaoBase):
    table = 'tbl_app_models'
    fields = ['id', 'software_id', 'model_id']


    def createTable(self):
        success = self.query.exec(f"""
            CREATE TABLE IF NOT EXISTS {self.table}(
                id INTEGER PRIMARY KEY,
                software_id INTEGER NOT NULL,
                model_id INTEGER NOT NULL,
                FOREIGN  KEY (software_id) REFERENCES tbl_app_info(id),
                FOREIGN  KEY (model_id) REFERENCES tbl_model_info(id)
            )
        """)
        return success