# coding:utf-8

'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-27 16:42:15
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-27 16:44:34
FilePath: \aistore\app\database\dao\sql_query.py
Description: dao - data model
'''

from app.common.logger import logger
from PyQt5.QtSql import QSqlQuery, QSqlError


class SqlQuery(QSqlQuery):
    """ Database sql statement execution class """

    def exec(self, query: str = None):
        """ execute sql statement """
        if not query:
            return self.check(super().exec())

        return self.check(super().exec(query))

    def check(self, success: bool):
        """ check execution result """
        if success:
            return True

        error = self.lastError()
        if error.isValid() and error.type() != QSqlError.NoError:
            msg = f'"{error.text()}" for query "{self.lastBoundQuery()}"'
            logger.error(msg)

        return False

    def lastBoundQuery(self):
        query = self.lastQuery()
        for k, v in self.boundValues().items():
            query = query.replace('?', str(v), 1)
            query = query.replace(k, str(v))

        return query
