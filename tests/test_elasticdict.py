import json
from operator import itemgetter
from pathlib import Path

import pytest

from elasticdict.elastic import ElasticDict
from .fixtures import FIXTURES


@pytest.fixture(params=FIXTURES)
def elastic_dict_obj(request):
    file = (Path(__file__).parent / 'fixtures' / request.param).read_text()
    data = json.loads(file)
    input_, asserts = itemgetter('input', 'asserts')(data)
    obj = ElasticDict(**input_)
    return obj, asserts


def test_ElasticDict__init__(elastic_dict_obj):
    obj, asserts = elastic_dict_obj

    assert isinstance(obj, ElasticDict)
    assert obj.step_dict == asserts.get('test_ElasticDict__init__')

