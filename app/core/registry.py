'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-19 17:19:07
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-21 14:22:47
FilePath: \aistore\app\core\registry.py
Description: read and write registry
'''
import winreg
import datetime
import os
from app.common.logger import logger

def write_install_info_to_registry(reg_path, display_name, display_version, publisher, install_date):
    """
    向注册表写入软件安装信息
    """
    # reg_path = r"Software\MySoftware"  # 自定义注册表路径
    try:
        # 打开或创建注册表键
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        
        # 写入注册表值
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, display_name)
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, display_version)
        winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, publisher)
        winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, install_date)
        
        # 关闭注册表键
        winreg.CloseKey(key)
        logger.info(f"软件安装信息已成功写入注册表：{reg_path}")
    except Exception as e:
        logger.error(f"写入注册表时出现错误：{e}")

def read_installed_software_from_registry(reg_path):
    """
    从注册表读取已安装的软件信息
    """
    software_list = []
    # reg_path = r"Software\MySoftware"  # 注册表路径
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        display_name, _ = winreg.QueryValueEx(key, "DisplayName")
        display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
        publisher, _ = winreg.QueryValueEx(key, "Publisher")
        install_date, _ = winreg.QueryValueEx(key, "InstallDate")
        
        software_info = {
            "DisplayName": display_name,
            "DisplayVersion": display_version,
            "Publisher": publisher,
            "InstallDate": install_date
        }
        
        software_list.append(software_info)
        
        winreg.CloseKey(key)
        
        return software_list
        
    except Exception as e:
        logger.error(f"读取注册表时出现错误：{e}")
        return software_list

def read_all_installed_software_from_registry(reg_path):
    """
    从注册表读取已安装的软件信息
    """
    software_list = []
    # reg_path = r"Software\MySoftware"  # 注册表路径
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
        index = 0
        while True:
            try:
                subkey_name = winreg.EnumKey(key, index)
                subkey_path = f"{reg_path}\\{subkey_name}"
                print(subkey_path)
                software_list += read_installed_software_from_registry(subkey_path)
            except Exception as e:
                break  # 如果无法获取某些值，跳过继续下一个
            
            index += 1
                
    except WindowsError as e:
        pass  # 到达注册表末尾，结束循环

    return software_list

def delete_software_registry_info(reg_path):
    """
    删除注册表中的 "FaceFusion" 软件信息
    """
    # reg_path = r"Software\MySoftware\FaceFusion"  # 注册表路径
    
    try:
        # 打开注册表键以进行删除
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
        logger.info(f"已成功删除 {reg_path} 的注册表信息")
    except WindowsError as e:
        logger.error(f"删除注册表时出现错误：{e}")   


# if __name__ == "__main__":
#     # 写入虚构的软件安装信息
#     software_name = "MySoftware1"
#     software_version = "1.0"
#     software_publisher = "MyCompany"
#     installation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     reg_path = os.path.join(r"Software\aistore", software_name)


#     write_install_info_to_registry(reg_path, software_name, software_version, software_publisher, installation_date)
    
#     # 读取已安装的软件信息
#     installed_software = read_installed_software_from_registry(reg_path)
#     if installed_software:
#         print("已安装的软件信息：")
#         for software in installed_software:
#             print(f"名称: {software['DisplayName']}")
#             print(f"版本: {software['DisplayVersion']}")
#             print(f"发布者: {software['Publisher']}")
#             print(f"安装日期: {software['InstallDate']}")
#             print()
#     else:
#         print("未找到已安装的软件信息。")

#     # 删除 "FaceFusion" 软件的注册表信息
#     delete_software_registry_info(reg_path)

