'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-21 14:48:05
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-21 15:00:40
FilePath: \aistore\app\bobject\app.py
Description: bo class of software
'''

class Software(object):
    def __init__(self, name, display_name, display_version, publisher, install_date, install_dir):
        self.name = name
        self.display_name = display_name
        self.display_version = display_version
        self.publisher = publisher
        self.install_date = install_date
        self.install_dir = install_dir

