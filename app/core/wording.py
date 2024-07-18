'''
Author: Firmin.Sun fmsunyh@gmail.com
Date: 2024-07-18 14:23:17
LastEditors: Firmin.Sun fmsunyh@gmail.com
LastEditTime: 2024-07-18 14:44:03
FilePath: \aistore\app\core\wording.py
Description: 
'''
from typing import Any, Dict, Optional
from ..common.config import Language, cfg

WORDING_CN: Dict[str, Any] = \
{
    "AI Painting": "AI 绘图",
    "Face Processing": "人脸处理",
    "Machine Learning": "机器学习",
    "AI Video": "AI 生成视频",
}

WORDING_EN: Dict[str, Any] = \
{
    "AI Painting": "AI Painting",
    "Face Processing": "Face Processing",
    "Machine Learning": "Machine Learning",
    "AI Video": "AI Video"
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