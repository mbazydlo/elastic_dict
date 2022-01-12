from dataclasses import dataclass

from elasticdict.utils import refresh_step_dict


class TestClass:
    def create_step_dict(self):
        self.value = 'value'


def test_refresh_step_dict():
    wrapper = refresh_step_dict(lambda arg: None)
    obj = TestClass()
    wrapper(obj)

    assert obj.value == 'value'
