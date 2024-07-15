from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FuzzyWuzzy:
    def __init__(self):
        self.keys = []
    
    def add_key(self, key):
        self.keys.append(key)

    def add_keys(self, keys: list):
        self.keys.extend(keys)

    def search(self, query, threshold=80):
        # 使用process.extract进行模糊匹配
        results = process.extract(query, self.keys, scorer=fuzz.partial_ratio)
        
        # 根据阈值过滤匹配结果， 返回index
        matched_indices = [self.keys.index(result[0]) for result in results if result[1] >= threshold]
        
        return matched_indices