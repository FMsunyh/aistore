'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 15:34:31
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-01 11:15:37
FilePath: \aistore\do_initializer_db.py
Description: initialize db
'''

import shutil
import sys
sys.path.insert(0, r'D:/aistore')

from app.database.db_initializer import DBInitializer
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from app.common.config import cfg
from app.common.logger import logger
import os


# 解析 XML 文件
def parse_xml(file):
    tree = ET.parse(file)
    return tree.getroot()

# 插入开发者数据
def insert_developers(cursor, root):
    for developer in root.findall('developer'):
        developer_id = int(developer.find('id').text)
        name = developer.find('name').text
        contact_info = developer.find('contactInfo').text
        website_url = developer.find('websiteURL').text
        
        cursor.execute('''
        INSERT INTO tbl_developers (id, name, contact_info, website_url)
        VALUES (?, ?, ?, ?)
        ''', (developer_id, name, contact_info, website_url))

# 插入软件类型数据
def insert_app_types(cursor, root):
    for type in root.findall('type'):
        type_id = int(type.find('id').text)
        name = type.find('name').text
        
        cursor.execute('''
        INSERT INTO tbl_app_types (id, name)
        VALUES (?, ?)
        ''', (type_id, name))

# 插入软件数据
def insert_app(cursor, root):
    for item in root.findall('item'):
        software_id = int(item.find('id').text)
        name = item.find('name').text
        icon = item.find('icon').text
        title = item.find('title').text
        type_id = int(item.find('typeId').text)
        developer_id = int(item.find('developerId').text)
        description = item.find('description').text
        release_date = item.find('releaseDate').text
        
        cursor.execute('''
        INSERT INTO tbl_app_info (id, name, icon, title, type_id, developer_id, description, release_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (software_id, name, icon, title, type_id, developer_id, description, release_date))

# 主程序
def init_from_xml(CACHE_FILE):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(CACHE_FILE)
    cursor = conn.cursor()
    
    # 插入数据
    developers_root = parse_xml(r'app\database\data\developers.xml')
    insert_developers(cursor, developers_root)
    
    software_types_root = parse_xml(r'app\database\data\app_types.xml')
    insert_app_types(cursor, software_types_root)
    
    software_root = parse_xml(r'app\database\data\app_info.xml')
    insert_app(cursor, software_root)
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()

    logger.info(f"Initialize the database from xml.")



if __name__ == '__main__':

    CACHE_FILE = str(Path(cfg.get(cfg.cacheFolder)) / "cache.db")

    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        logger.info(f"remove file {CACHE_FILE}.")

    else:
        logger.info(f"The file {CACHE_FILE} does not exist.")

    DBInitializer.init()
    init_from_xml(CACHE_FILE)


    install_source =r'.install\source\app\cache\cache.db'
    if os.path.exists(install_source):
        os.remove(install_source)
        logger.info(f"remove file {install_source}.")

    else:
        logger.info(f"The file {install_source} does not exist.")
    
    shutil.copyfile(CACHE_FILE, install_source)
    logger.info(f"Copy file {CACHE_FILE} to {install_source}.")