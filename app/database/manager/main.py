import sqlite3
import xml.etree.ElementTree as ET

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
def main():
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(r'D:\aistore\app\cache\cache.db')
    cursor = conn.cursor()
    
    # 插入数据
    developers_root = parse_xml(r'D:\aistore\app\database\manager\data\developers.xml')
    insert_developers(cursor, developers_root)
    
    software_types_root = parse_xml(r'D:\aistore\app\database\manager\data\app_types.xml')
    insert_app_types(cursor, software_types_root)
    
    software_root = parse_xml(r'D:\aistore\app\database\manager\data\app_info.xml')
    insert_app(cursor, software_root)
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
