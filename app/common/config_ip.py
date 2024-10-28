'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-29 11:46:34
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-29 15:41:46
FilePath: \aistore\app\common\config_ip.py
Description: 
'''
from pathlib import Path
import socket
import geoip2.database
from app.common.logger import logger

'''
aistore.1pluslive.com  120.233.206.35
aistorehk.1pluslive.com 45.254.27.97
'''
HONG_KONG_IP = 'aistorehk.1pluslive.com'
DOMESTIC_IP = 'aistore.1pluslive.com'

def get_external_ip():
    # Get the hostname
    hostname = socket.gethostname()

    # Get the local IP address
    local_ip = socket.gethostbyname(hostname)

    logger.info(f"Hostname: {hostname}")
    logger.info(f"Local IP address: {local_ip}")

    import requests

    # Get the external IP address
    external_ip = requests.get('https://api.ipify.org').text

    logger.info(f"External IP address: {external_ip}")

    return external_ip

def is_hong_kong(ip_address,database):
    hong_kong = False
    # Open the GeoLite2 database
    with geoip2.database.Reader(database) as reader:
        response = reader.city(ip_address)

        if response.city.name == 'Hong Kong':
            logger.info(f"IP address {ip_address} is in Hong Kong")
            hong_kong = True
        else:
            logger.info(f"IP address {ip_address} is not in Hong Kong")

        logger.info(f"City: {response.city.name}")
    return hong_kong

# def CONFIG_IP(GeoLite2_database):
#     ip_address = get_external_ip()
#     hong_kong = is_hong_kong(ip_address,GeoLite2_database)
#     if hong_kong:
#         return HONG_KONG_IP
#     else:
#         return DOMESTIC_IP

# 配置内网IP，之前的公网不要了
# Add 2024.10.28
def CONFIG_IP(GeoLite2_database):
    return "172.30.5.254"