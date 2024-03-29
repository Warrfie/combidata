import random
from pprint import pprint

import pytest
from combidata.classes.case import Case

from combidata.classes.combination import Combination

from combidata import ST_COMBINE, ST_GENERATE, ST_FORM, DataGenerator, Process
from re_generate import re_generate

from combidata.funcs.exeptions import CombinatoricsError


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
        "inc": "SAVES",
        "obj1": "OBJ1",
        "obj2": "OBJ2",
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
library["cases"]["OBJ1"] = {
    "1": {
        "gen_func": re_generate,
        "value": r"[a-zA-Z]{50}",
        "requirements": {"CODE": "NT"},
        "name": "1Standart NAME check"
    },
    "2": {
        "value": "12345",
        "requirements": {"CODE": "NT"},
        "name": "1Check NAME with error"
    },
    "3": {
        "value": None,
        "requirements": {"OBJ2": ["1", "2"]},
        "is_presented": False,
        "name": "1Check NAME for not necessary field"
    }}
library["cases"]["OBJ2"] = {
    "1": {
        "gen_func": re_generate,
        "value": r"[a-zA-Z]{50}",
        "name": "2Standart NAME check"
    },
    "2": {
        "value": "12345",
        "name": "2Check NAME with error"
    },
    "3": {
        "value": None,
        "requirements": {"CODE": "T"},
        "is_presented": False,
        "name": "2Check NAME for not necessary field"
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
    "Case": {
        "value": "CASE",
        "name": "Case CODE"
    }
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

generator = DataGenerator(library)


generator.run()


@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test_smoke(combination_name):
    combination = generator.combinations[combination_name]
    combination.run()
    if isinstance(combination.step_done, Exception):
        raise combination.step_done
    print()
    print(combination.test_seed)
    print()
    pprint(combination.formed_data)


@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test_smoke(combination_name):
    combination = generator.combinations[combination_name]
    combination.run()
    if isinstance(combination.step_done, CombinatoricsError):
        pytest.skip()
    elif isinstance(combination.step_done, Exception):
        raise combination.step_done
    print()
    print(combination.test_seed)
    print()
    pprint(combination.formed_data)
    assert combination.test_seed.get("OBJ2", True) != "3"


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


@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test3(combination_name):
    combination = generator.combinations[combination_name]
    seed = combination.test_seed
    key = random.choice(list(seed.keys()))
    seed = {key: seed[key]}
    print(seed)
    semi_gen = DataGenerator(library, possible_modes=seed, amount=100)
    semi_gen.run()
