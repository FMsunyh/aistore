'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-28 15:34:31
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-03 18:16:39
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
        brief_introduction = item.find('briefIntroduction').text
        description = item.find('description').text
        release_date = item.find('releaseDate').text
        
        cursor.execute('''
        INSERT INTO tbl_app_info (id, name, icon, title, type_id, developer_id, description, brief_introduction, release_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (software_id, name, icon, title, type_id, developer_id, description,brief_introduction, release_date))

# 插入许可证数据
def insert_licenses(cursor, root):
    for license in root.findall('license'):
        license_id = int(license.find('id').text)
        software_id = int(license.find('softwareId').text)
        license_key = license.find('licenseKey').text
        release_date = license.find('releaseDate').text
        expiry_date = license.find('expiryDate').text
        license_type = license.find('licenseType').text
        
        cursor.execute('''
        INSERT INTO tbl_licenses (id, software_id, license_key, release_date, expiry_date, license_type)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (license_id, software_id, license_key, release_date, expiry_date, license_type))

# 插入用户数据
def insert_users(cursor, root):
    for user in root.findall('user'):
        user_id = int(user.find('id').text)
        user_name = user.find('userName').text
        email = user.find('email').text
        password = user.find('password').text
        
        cursor.execute('''
        INSERT INTO tbl_user (id, name, email, password)
        VALUES (?, ?, ?, ?)
        ''', (user_id, user_name, email, password))

# 插入用户软件数据
def insert_user_software(cursor, root):
    for entry in root.findall('entry'):
        user_software_id = int(entry.find('id').text)
        user_id = int(entry.find('userId').text)
        software_id = int(entry.find('softwareId').text)
        license_id = int(entry.find('licenseId').text)
        install_date = entry.find('installDate').text
        is_installed = int(entry.find('isInstalled').text)
        
        cursor.execute('''
        INSERT INTO tbl_user_app (id, user_id, software_id, license_id, install_date, is_installed)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_software_id, user_id, software_id, license_id, install_date, is_installed))

# 插入评分和评论数据
def insert_ratings_reviews(cursor, root):
    for rating_review in root.findall('rating_review'):
        rating_review_id = int(rating_review.find('id').text)
        software_id = int(rating_review.find('softwareId').text)
        user_id = int(rating_review.find('userId').text)
        rating = int(rating_review.find('rating').text)
        review = rating_review.find('review').text
        review_date = rating_review.find('reviewDate').text
        
        cursor.execute('''
        INSERT INTO tbl_ratings_reviews (id, software_id, user_id, rating, review, review_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (rating_review_id, software_id, user_id, rating, review, review_date))

# 插入截图数据
def insert_screenshots(cursor, root):
    for screenshot in root.findall('screenshot'):
        screenshot_id = int(screenshot.find('id').text)
        software_id = int(screenshot.find('softwareId').text)
        image_url = screenshot.find('imageURL').text
        description = screenshot.find('description').text
        upload_date = screenshot.find('uploadDate').text
        
        cursor.execute('''
        INSERT INTO tbl_screenshots (id, software_id, image_url, description, upload_date)
        VALUES (?, ?, ?, ?, ?)
        ''', (screenshot_id, software_id, image_url, description, upload_date))

# 插入版本信息数据
def insert_app_versions(cursor, root):
    for version in root.findall('version'):
        version_id = int(version.find('id').text)
        software_id = int(version.find('softwareId').text)
        version_number = version.find('versionNumber').text
        release_date = version.find('releaseDate').text
        change_log = version.find('changelog').text
        
        cursor.execute('''
        INSERT INTO tbl_app_versions (id, software_id, version_number, release_date, change_log)
        VALUES (?, ?, ?, ?, ?)
        ''', (version_id, software_id, version_number, release_date, change_log))

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
    
    licenses_root = parse_xml(r'app\database\data\licenses.xml')
    insert_licenses(cursor, licenses_root)
    
    users_root = parse_xml(r'app\database\data\users.xml')
    insert_users(cursor, users_root)
    
    user_software_root = parse_xml(r'app\database\data\user_software.xml')
    insert_user_software(cursor, user_software_root)
    
    ratings_reviews_root = parse_xml(r'app\database\data\ratings_reviews.xml')
    insert_ratings_reviews(cursor, ratings_reviews_root)
    
    screenshots_root = parse_xml(r'app\database\data\screenshots.xml')
    insert_screenshots(cursor, screenshots_root)

    app_versions_root = parse_xml(r'app\database\data\app_versions.xml')
    insert_app_versions(cursor, app_versions_root)

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