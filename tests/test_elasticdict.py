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


def test_create_instance_elasticdict(prepare_dictionary):
    obj = ElasticDict(prepare_dictionary)
    assert obj


def test_parse_string_keys(prepare_dictionary):
    result = ElasticDict(prepare_dictionary)._parse_string_keys("key1,key2,key3")
    assert result == ["key1", "key2", "key3"]