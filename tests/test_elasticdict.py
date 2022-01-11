import json
from operator import itemgetter
from pathlib import Path

import pytest

from elasticdict.elastic import ElasticDict

FIXTURES = (
    'fixture_1.json',
    'fixture_2.json', 
    'fixture_3.json',
)

@pytest.fixture(params=FIXTURES)
def elastcit_dict_obj(request):
    file = ( Path(__file__).parent / 'fixtures' / request.param ).read_text()
    data = json.loads(file)
    input, asserts = itemgetter('input', 'asserts')(data)
    obj = ElasticDict(**input)
    return obj, asserts

def test_ElasticDict__init__(elastcit_dict_obj):
    obj, asserts = elastcit_dict_obj

    assert isinstance(obj, ElasticDict)
    assert obj.step_dict == asserts.get('test_ElasticDict__init__')