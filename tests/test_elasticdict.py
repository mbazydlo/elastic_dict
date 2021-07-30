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

@pytest.fixture(params=[(f'dictionary_{number}.json', f'target_dictionary_{number}.json') for number in range(1, 4)])
def prepare_source_and_target_dictionary(request):
    location_source_dict = os.path.join(os.getcwd(), 'tests', 'fixtures', request.param[0])
    location_target_dict = os.path.join(os.getcwd(), 'tests', 'fixtures', request.param[1])

    with (open(location_source_dict, encoding='utf-8') as source_file,
        open(location_target_dict, encoding='utf-8') as target_file):

        test_source_dictionary = json.load(source_file)
        test_target_dictionary = json.load(target_file)
    
    return test_source_dictionary, test_target_dictionary


def test_create_instance_elasticdict(prepare_dictionary):
    obj = ElasticDict(prepare_dictionary)
    assert isinstance(obj, ElasticDict)


def test_parse_string_keys(prepare_dictionary):
    result_coma = ElasticDict(prepare_dictionary)._parse_string_keys("key1,key2,key3")
    result_dot = ElasticDict(prepare_dictionary)._parse_string_keys("key1.key2.key3", delimiter='.')
    result_semicolon = ElasticDict(prepare_dictionary)._parse_string_keys("key1;key2;key3", delimiter=';')
    assert result_coma == ["key1", "key2", "key3"]
    assert result_dot == ["key1", "key2", "key3"]
    assert result_semicolon == ["key1", "key2", "key3"]


def test_get_keys_from_string_keys(prepare_nesteted_dictionary):
    assert prepare_nesteted_dictionary.get("address", {}).get("number", {}) == 1
    assert prepare_nesteted_dictionary.get("address", {}).get("nonExisting", {}) == {}

def test_load_to_target_dict(prepare_dictionary):
    obj = ElasticDict(prepare_dictionary)
    for key, value in obj.source_dict.items():
        obj._load_to_target_dict(key, value)

    list_of_value_types = [value.__class__.__name__ for value in obj.target_dict.values()]

    assert isinstance(obj.target_dict, dict)

    if list_of_value_types:
        is_all_list_type = map(lambda type_: type_ == 'list', list_of_value_types)
        assert any(is_all_list_type)

def test_parse_source_dict(prepare_source_and_target_dictionary):
    obj = ElasticDict(prepare_source_and_target_dictionary[0])
    obj.parse_source_dict()
    assert isinstance(obj.target_dict, dict)
    assert obj.target_dict == prepare_source_and_target_dictionary[1]

def test_str(prepare_source_and_target_dictionary):
    obj = ElasticDict(prepare_source_and_target_dictionary)
    assert str(obj.target_dict) == str(obj)
    assert str(obj.target_dict) != str({1: 1})

def test_repr(prepare_source_and_target_dictionary):
    obj = ElasticDict(prepare_source_and_target_dictionary)
    assert obj.__repr__() == f"ElasticDict[{obj.target_dict}]"
    assert obj.__repr__() != "ElasticDict[{1: 1}]"

def test_delitem(prepare_source_and_target_dictionary):
    obj = ElasticDict(prepare_source_and_target_dictionary)
    if obj:
        del obj["name"]
        prepare_source_and_target_dictionary[1].pop("name")
        assert obj.target_dict == prepare_source_and_target_dictionary[1]
