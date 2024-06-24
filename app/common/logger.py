'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-06-24 23:51:48
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-06-25 00:21:38
FilePath: \aistore\app\common\logger.py
Description: logger
'''
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

# 创建一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 自定义日志文件名格式，带日期
log_filename = datetime.datetime.now().strftime('aistore_%Y-%m-%d.log')

# 创建一个定时轮换文件处理程序，每天生成一个新的日志文件
file_handler = TimedRotatingFileHandler(log_filename, when='midnight', interval=1, backupCount=7, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.suffix = "%Y-%m-%d"  # 设置后缀为日期格式

# 创建一个日志格式器并设置格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 创建一个控制台处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# 将处理程序添加到记录器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
