'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-18 14:23:17
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-19 18:20:10
FilePath: \aistore\app\core\wording.py
Description: 
'''
from typing import Any, Dict, Optional
from ..common.config import Language, cfg

WORDING_CN: Dict[str, Any] = \
{
    "app_type" : {    
        "AI Painting": "AI 绘图",
        "Face Processing": "人脸处理",
        "Machine Learning": "机器学习",
        "AI Video": "AI 生成视频",
        "Pytorch": "Pytorch"
    },

    "table" : {
        "id": "序号",
        "name": "名称",
        "author": "作者",
        "type_id": "类型ID",
        "download_url": "下载地址",
        "file_name": "文件名称",
        "description": "描述",
        "size": "大小"
    }
    
}

WORDING_EN: Dict[str, Any] = \
{
    "app_type" : {    
        "AI Painting": "AI Painting",
        "Face Processing": "Face Processing",
        "Machine Learning": "Machine Learning",
        "AI Video": "AI Video",
        "Pytorch": "Pytorch",
    },
    "table" : {
        "id": "ID",
        "name": "name",
        "author": "author",
        "type_id": "type ID",
        "download_url": "download url",
        "file_name": "file name",
        "description": "description",
        "size": "size"
    },
}
def get(key : str) -> Optional[str]:
    language = cfg.get(cfg.language) 
    if language == Language.CHINESE_SIMPLIFIED:
        WORDING =  WORDING_CN
    else:
         WORDING =  WORDING_EN

    if '.' in key:
        section, name = key.split('.')
        if section in WORDING and name in WORDING[section]:
            return WORDING[section][name]
    if key in WORDING:
        return WORDING[key]
    return None