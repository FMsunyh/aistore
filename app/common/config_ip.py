'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-29 11:46:34
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-29 14:16:56
FilePath: \aistore\app\common\config_ip.py
Description: 
'''
from pathlib import Path
import socket
import geoip2.database
from app.common.logger import logger

HONG_KONG_IP = '45.254.27.97'
DOMESTIC_IP = '120.233.206.35'

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

def CONFIG_IP(GeoLite2_database):
    ip_address = get_external_ip()
    hong_kong = is_hong_kong(ip_address,GeoLite2_database)
    if hong_kong:
        return HONG_KONG_IP
    else:
        return DOMESTIC_IP