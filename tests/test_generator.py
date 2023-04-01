from pprint import pprint

import pytest
from combidata.classes.case import Case

from combidata.classes.combination import Combination

from combidata import ST_COMBINE, ST_GENERATE, ST_FORM, DataGenerator, Process
import re_generate

re_generate = re_generate.get_str


def code_generator(combination, example_token):
    # just for test
    return "12GG233"

def gen_comb(combination: Combination):
    new_comb = DataGenerator(library, amount=1).get_one()
    new_comb.run()
    return new_comb.generated_data

def gen_smile():
    return ":)"

def gen_value(value):
    return value


library = {
    "cases": {},
    "workflow": (ST_COMBINE, ST_GENERATE, ST_FORM),
    "tools": {},
    "template": {
        "NAME": "NAME",
        "code": "CODE",
        "inc": "SAVES"
    }
}
library["cases"]["NAME"] = {
    "TfNN": {
        "gen_func": re_generate,
        "value": r"[a-zA-Z]{50}",
        "name": "Standart NAME check"
    },
    "FfNN": {
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
    "TNNN": {
        "gen_func": code_generator,
        "value": "token",
        "options": {"combination": "combination", "example_token": "wa69sf"},
        "name": "Standart CODE check"
    },
    "NT": {
        "value": None,
        "is_presented": False,
        "name": "Check CODE for not necessary field"
    },
    "T": {
        "value": "wa69sf",
        "name": "Example CODE"
    },
    "Case": Case({
        "value": "wa69sf",
        "name": "Example Case"
    }, "CODE", "Case")
}
library["cases"]["SAVES"] = {
    "None": {
        "is_presented": False,
        "name": "No SAVES"
    },
    "sAVED": {
        "gen_func": gen_comb,
        "options": {"combination": "combination"},
        "name": "Exp SAVES"
    },
    "nO ARGS": {
        "gen_func": gen_smile,
        "options": {},
        "name": "Exp smile"
    },
    "Only value": {
        "value": "Hi",
        "gen_func": gen_value,
        "options": {"value": "value"},
        "name": "Exp Hi"
    },
}



generator = DataGenerator(library, amount=100)
generator.run()


@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test(combination_name):
    combination = generator.combinations[combination_name]
    print()
    assert combination.test_seed != {'CODE': 'N', 'NAME': 'N'}
    print(combination.test_seed)
    print()
    pprint(combination.formed_data)


@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test2(combination_name):
    combination = generator.combinations[combination_name]
    seed = combination.test_seed
    print()
    print(seed)
    gen_seed: Combination = DataGenerator(library, possible_modes=seed, amount=1).get_one()
    gen_seed.run()
    gen_seed = gen_seed.test_seed
    assert seed == gen_seed
