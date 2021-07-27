import pytest

from ..run import ElasticDict

def test_create_instance_elasticdict():
    obj = ElasticDict({})
    assert obj