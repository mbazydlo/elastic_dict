"""
Ready for documentation.
"""
from collections.abc import MutableMapping


class ElasticDict(MutableMapping):
    def __init__(self, source_dict: dict = None, **kwargs):
        if source_dict and self._check_input_type(source_dict):
            self.source_dict = source_dict
        else:
            self.source_dict = kwargs
        self.target_dict = dict()
        self.parts = list()
        self.delimiter = kwargs.get('delimiter', '.')

        self.create_step_dict()
    
    def __getitem__(self, key: str):
        """
        Returns value for passed key.
        It accepts single key as well as multiples splited by self.delimiter

        ex.
        obj.get('key1.key2.key3')

        :param str key:
        :return: value for passed key
        """

        if self.delimiter not in key:
            return self.source_dict.get(key)
        else:
            return self.get_value_from_string_keys(key)

    def __setitem__(self, key, value):
        if self.delimiter not in key:
            self.target_dict[key] = value
        else:
            keys = key.split('.')
            dict_ = self.source_dict

            for index, single_key in enumerate(keys[:-1], start=1):
                dict_ = dict_.setdefault(single_key, {})

            dict_[keys[-1]] = value

        self.target_dict[key] = value

    def __delitem__(self, key):
        del self.source_dict[key]

    def __iter__(self):
        return iter(self.source_dict)
    
    def __len__(self):
        return len(self.source_dict)
    
    def __str__(self):
        return str(self.source_dict)

    def __repr__(self):
        return str(self.source_dict)
    
    def _check_input_type(self, value):
        if value.__class__ not in (dict,):
            raise TypeError('Input is not a dict')
        return True

    def get_all(self, key: str, only: str = None, exclude: str = None):
        """
        Generates all values that match to the passed key.

        :param str key:
        :param str only:
        :param str exclude:
        :return: The list of values of all keys
        :rtype: list
        """

        found_keys = []
        for key_, value in self.target_dict.items():

            conditions = [
                key_.endswith(self.delimiter + key) or not key_.strip(key),
                value.startswith(only) if only else True,
                not value.startswith(exclude) if exclude else True
            ]
            
            if all(conditions):
                found_keys.append(value)

        return found_keys
    
    def get_one(self, key):
        """
        Returns first key of matches.

        :param str key: The key to be find in target_dict
        :return: The value of first key
        :rtype: str
        """
        return result[0] if (result := self.get_all(key)) else None

    def _parse_string_keys(self, keys_as_string):
        list_of_keys = keys_as_string.split(self.delimiter)
        return list_of_keys
    
    def get_value_from_string_keys(self, keys_as_string):
        list_of_keys = self._parse_string_keys(keys_as_string)
        temporary_dict = self.source_dict
        
        for key in list_of_keys:
            temporary_dict = temporary_dict.get(key, dict())
        
        return temporary_dict
    
    def create_step_dict(self, value=None):
        if not value:
            value = self.source_dict

        for key, value in value.items():
            self.parts.append(key)
            
            if isinstance(value, dict):
                self.create_step_dict(value)
            else:
                self.target_dict['.'.join(self.parts)] = value
            self.parts.pop()

