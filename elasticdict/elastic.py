"""
Ready for documentation.
"""
from collections.abc import MutableMapping, KeysView, ValuesView, ItemsView
from typing import Dict, Any, List, Union
import re

from errors import DuplicatedKeyError
from utils import refresh_step_dict


class ElasticDict(MutableMapping):

    @refresh_step_dict
    def __init__(self, source_dict: dict = None, *, delimiter='.', default=None, **kwargs):
        if source_dict and self._check_input_type(source_dict):
            self.source_dict = source_dict
        else:
            self.source_dict = kwargs
        self.step_dict = dict()
        self.parts = list()
        self.delimiter = delimiter
        self.default = default
    
    def __getitem__(self, key: str, value=None):
        """
        Returns value for passed key.
        It accepts single key as well as multiples splited by self.delimiter

        ex.
        obj.get('key1.key2.key3')

        :param str key:
        :return: value for passed key
        """

        if self.delimiter not in key:
            return self.source_dict.get(key, value or self.default)
        else:
            return self.get_value_from_string_keys(key, value or self.default)

    def __setitem__(self, key, value):
        if self.delimiter not in key:
            self.step_dict[key] = value
        else:
            keys = key.split('.')
            dict_ = self.source_dict

            for index, single_key in enumerate(keys[:-1], start=1):
                dict_ = dict_.setdefault(single_key, {})

            dict_[keys[-1]] = value

        self.step_dict[key] = value

    def __delitem__(self, key):
        *keys, last_key = key.split('.')

        to_delete = self.get('.'.join(keys))
        del to_delete[last_key]
        del self.step_dict[key]

    def __iter__(self):
        return iter(self.source_dict)
    
    def __len__(self):
        return len(self.source_dict)

    def __repr__(self):
        return f'ElasticDict[{self.source_dict}]'

    def __eq__(self, other: Union[dict, MutableMapping]):
        if isinstance(other, dict):
            return self.step_dict == other
        elif isinstance(other, ElasticDict):
            return self.step_dict == other.step_dict
        else:
            raise TypeError(f'{other} should be dict or ElasticDict type, not {other.__class__}')
    
    def _check_input_type(self, value) -> bool:
        if value.__class__ not in (dict,):
            raise TypeError('Input is not a dict')
        return True

    def get_all(
            self,
            key: str,
            only: str = None,
            exclude: str = None,
            min_depth: int = 1,
            max_depth: int = 100
    ) -> List[Any]:
        """
        Generates all values that match to the passed key.

        :param str key:
        :param str only:
        :param str exclude:
        :param str min_depth:
        :param str max_depth:
        :return: The list of values of all keys
        :rtype: list
        """

        found_keys = []

        # Slicing source dictionary if min_depth or max_depth provided
        if min_depth or max_depth:
            target_dict = self._select_min_max_depth_data(min_depth, max_depth)
        else:
            target_dict = self.step_dict

        for key_, value in target_dict.items():

            conditions = [
                key_.endswith(self.delimiter + key) or not key_.strip(key),
                value.startswith(only) if only else True,
                not value.startswith(exclude) if exclude else True
            ]
            
            if all(conditions):
                found_keys.append(value)

        return found_keys
    
    def get_one(
            self,
            key: str,
            unique=False,
            min_depth: int = 1,
            max_depth: int = 100,
    ) -> Any:
        """
        Returns first key of matches.

        :param str key: The key to be find in step_dict
        :param bool unique:
        :param int min_depth:
        :param int max_depth:DuplicatedKeyError
        :return: The value of first key
        :rtype: str
        """

        result = self.get_all(key, min_depth=min_depth, max_depth=max_depth)
        if unique and (len_ := len(result)) > 1:
            raise DuplicatedKeyError(f'The provided key is not unique. In occurs in at {len_} places', result)

        return result[0] if result else None

    def _select_min_max_depth_data(self, min_depth, max_depth):
        target_dict = {
            key: value for key, value in self.step_dict.items() if min_depth <= key.count('.') + 1 <= max_depth
        }
        return target_dict

    def _parse_string_keys(self, keys_as_string: str) -> List[str]:
        list_of_keys = keys_as_string.split(self.delimiter)
        return list_of_keys

    def _if_array_return_slice(self, key: str) -> Union[List[str], None]:
        if match := re.search('\[.+\]', key).group():
            return match.strip('[').strip(']').split(':')

    def get_value_from_string_keys(self, keys_as_string: str, value=None):
        *keys, last_key = self._parse_string_keys(keys_as_string)
        temporary_dict = self.source_dict
        
        for key in keys:
            temporary_dict = temporary_dict.get(key, dict())

        temporary_dict = temporary_dict.get(last_key, value)
        return temporary_dict
    
    def create_step_dict(self, value: Dict[str, Any] = None):
        if not value:
            value = self.source_dict

        for key, value in value.items():
            self.parts.append(key)
            
            if isinstance(value, dict):
                self.create_step_dict(value)
            else:
                self.step_dict['.'.join(self.parts)] = value
            self.parts.pop()

    def flatted_keys(self, unique_only: bool = False) -> Dict[str, Any]:
        flatted_dict = dict()
        non_unique_keys = set()

        for key, value in self.step_dict.items():
            *_, flatted_key = key.split(self.delimiter)

            if unique_only and (flatted_key in flatted_dict):
                non_unique_keys.add(flatted_key)
                continue

            flatted_dict[flatted_key] = value

        if non_unique_keys:
            raise DuplicatedKeyError(
                f'Dictionary cannot be flatted as there are non unique keys: {non_unique_keys}'
            )
        return flatted_dict

    @refresh_step_dict
    def update(self, other):
        self.source_dict.update(other)

    def keys(self, source: str = 'source_dict') -> KeysView:
        return self.__getattribute__(source).keys()

    def values(self, source: str = 'source_dict') -> ValuesView:
        return self.__getattribute__(source).values()

    def items(self, source: str = 'source_dict') -> ItemsView:
        return self.__getattribute__(source).items()

    def elastic_keys(self) -> KeysView:
        return self.keys('step_dict')

    def elastic_values(self) -> ValuesView:
        return self.values('step_dict')

    def elastic_items(self) -> ItemsView:
        return self.items('step_dict')



