import pytest

from combidata import ST_COMBINE, ST_GENERATE, ST_FORM, DataGenerator
import re_generate

re_generate = re_generate.get_str
def code_generator(value, combination, example_token):
    # just for test
    return "12GG233"

library = {
    "cases": {},
    "workflow": (ST_COMBINE, ST_GENERATE, ST_FORM),
    "tools": {},
    "template": {
        "NAME": "NAME",
        "code": "CODE"
    }
}
library["cases"]["NAME"] = {
    "T": {
        "gen_func": re_generate,
        "value": r"[a-zA-Z]{50}",
        "name": "Standart NAME check"
    },
    "F": {
        "value": "12345",
        "type": "error",
        "name": "Check NAME with error"
    },
    "N": {
        "value": None,
        "requirements": {"CODE": "T"},
        "is_presented": False,
        "name": "Check NAME for not necessary field"
    }}
library["cases"]["CODE"] = {
    "T": {
        "gen_func": code_generator,
        "value": "token",
        "options": {"combination": "combination", "example_token": "wa69sf"},
        "name": "Standart CODE check"
    },
    "N": {
        "value": None,
        "is_presented": False,
        "name": "Check CODE for not necessary field"
    }
}

generator = DataGenerator(library)
generator.run()
@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test(combination_name):
    combination = generator.combinations[combination_name]
    print()
    assert combination.test_seed != {'CODE': 'N', 'NAME': 'N'}
    print(combination.test_seed)
    print()
    print(combination.generated_data)