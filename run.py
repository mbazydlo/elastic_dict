"""
Ready for documentation.
"""

class ElasticDict:
    def __init__(self, source_dict):
        self.source_dict = source_dict
        self.target_dict = dict()

    def _parse_string_keys(self, keys_as_string, delimiter=','):
        list_of_keys = keys_as_string.split(delimiter)
        return list_of_keys
    
    def get_value_from_string_keys(self, keys_as_string, delimiter=','):
        list_of_keys = self._parse_string_keys(keys_as_string, delimiter=',')
        temporary_dict = self.source_dict
        
        for key in list_of_keys:
            temporary_dict = temporary_dict.get(key, dict())
        
        return temporary_dict
    
    def _collect_all_keys(self, key, value):
        if key not in self.target_dict:
            self.target_dict[key] = [value]
        else:
            self.target_dict[key].append(value)
    
    def parse_source_dict(self, level_dict):
        if not level_dict:
            level_dict = self.source_dict
        
        for key, value in level_dict.items():
            self._collect_all_keys(key, value)
            
            if isinstance(value, dict):
                self.parse_source_dict(value)
