"""
Ready for documentation.
"""

class ElasticDict:
    def __init__(self, source_dict):
        self.source_dict = source_dict

    def _parse_string_keys(self, keys_as_string, delimiter=','):
        list_of_keys = keys_as_string.split(delimiter)
        return list_of_keys