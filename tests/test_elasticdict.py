import os
import json
import pytest

from ..run import ElasticDict

@pytest.fixture(params=[f'dictionary_{number}.json' for number in range(1, 4)])
def prepare_dictionary(request):
    location = os.path.join(os.getcwd(), 'tests', 'fixtures', request.param)

    with open(location, encoding='utf-8') as file:
        test_dictionary = json.load(file)
    
    return test_dictionary

@pytest.fixture()
def prepare_nesteted_dictionary():
    location = os.path.join(os.getcwd(), 'tests', 'fixtures', 'dictionary_3.json')

    with open(location, encoding='utf-8') as file:
        test_dictionary = json.load(file)
    
    return test_dictionary


def test_create_instance_elasticdict(prepare_dictionary):
    obj = ElasticDict(prepare_dictionary)
    assert obj


def test_parse_string_keys(prepare_dictionary):
    result = ElasticDict(prepare_dictionary)._parse_string_keys("key1,key2,key3")
    assert result == ["key1", "key2", "key3"]


def test_get_keys_from_string_keys(prepare_nesteted_dictionary):
    assert prepare_nesteted_dictionary.get("address", {}).get("number", {}) == 1
    assert prepare_nesteted_dictionary.get("address", {}).get("nonExisting", {}) == {}

def test_collect_all_keys(prepare_dictionary):
    obj = ElasticDict(prepare_dictionary)
    for key, value in obj.source_dict.items():
        obj._collect_all_keys(key, value)

    list_of_value_types = [value.__class__.__name__ for value in obj.target_dict.values()]

    assert isinstance(obj.target_dict, dict)

    if list_of_value_types:
        is_all_list_type = map(lambda type_: type_ == 'list', list_of_value_types)
        assert any(is_all_list_type)