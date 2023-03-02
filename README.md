[![PyPi Package Version](https://img.shields.io/pypi/v/combidata.svg)](https://pypi.python.org/pypi/combidata)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/combidata.svg)](https://pypi.python.org/pypi/combidata)
[![PyPi status](https://img.shields.io/pypi/status/combidata.svg?style=flat-square)](https://pypi.python.org/pypi/combidata)

# <p align="center">Combidata

<p align="center">A simple and light package for QA development which can generate random data from given cases.</p>
The main mechanics of the library is DataGenerator instance consume test flags and dictionary
with all cases, form and workflow. Creates Combination instances from possible cases. 
Via run function combination processes all steps from workflow.

###<p align="center">Structure of input library

```python
library = {
            "cases": {},
            "workflow": (ST_COMBINE, ST_GENERATE, ST_FORM),
            "tools": {},
            "template": {}
}
```

Key "cases" holds only lib instance with all your cases
Key "workflow" holds list or tuple with processes
Key "tools" holds dictionary with items which can be used in processes
Key "template" holds a template for export result

###<p align="center">Cases

Cases structure hold fields names as keys and every field name holds field cases codes as a keys
and every field cases codes holds case structure. 
I know, very complicate, but example will help you:

```python
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
```
Let's know about keys in case structure:
"name" - (string) necessary value and must be uniq. If that case is major - all combination unit will hand it
"gen_func" - (function) holds function for generation by default takes only one argument
"value" - (anything) holds case value it will be first argument of gen_func if gen_func in case 
"options" - (dictionary) holds functions nd another stuff which will unpack into gen_func. "combination" is reserved string
"is_presented" - (boolean) holds flag for export function. It will be not exported if False.
"requirements" - (dictionary) holds possible modes of another fields
"type" - (string) Generator will choose that case like main case when you will run test of that type

###<p align="center">Workflow

Holds tuple of processes or list of processes. When you will run combination or generator it will run all processes in tuple
Also yoy can use dict for hold workflow for tests with different types. "standard" is reserved key for standard workflow

```python
"workflow": (ST_COMBINE, ST_GENERATE, ST_FORM)
or 
"workflow": [(ST_COMBINE, ST_GENERATE, ST_FORM), (ANOTHER_STEP)]
or 
"workflow": {
    "standard": (ST_COMBINE, ST_GENERATE, ST_FORM),
    "error": [(ST_COMBINE, ST_GENERATE, ST_FORM), (ANOTHER_STEP)]
}
```

don't forget use another run if you use list workflow

about processes, feed Process instance with process name and process function

```python
ST_COMBINE = Process("ST_COMBINE", combine)
```
Process must return True when it over or Generator will run it infinitely
you can stop all workflow just put in combination.step_done reserved string "STOP"
```python
combination.step_done = "STOP"
```

###<p align="center">Tools
Just warehouse for items, funcs or other stuff that you can use in steps or generators via .tools
```python
"tools": {
    "UTILS": utilites,
    "TOKEN": token_generator
}

#....

block = combination.tools["UTILS"].get_block()

```

###<p align="center">Template
Holds template of generation result. All case codes will be reserved and will be replaced in template
like that
```python
"template": {
    "NAME": "NAME",
    "code": "CODE"
}
```
Result will look like 

    {"NAME": "azRkdSS", "code": "12GG233"}

###<p align="center">Example

```python
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
```

It will print in console
```
PASSED                      [ 25%]
{'NAME': 'T', 'CODE': 'T'}

{'NAME': 'OexmkFKlAyJkNqNHLnoGkcCgNmGkCVkAfHvOWeNfwEFeyhCjAt', 'CODE': '12GG233'}
PASSED       [ 50%]
{'NAME': 'N', 'CODE': 'T'}

{'CODE': '12GG233'}
PASSED                      [ 75%]
{'CODE': 'T', 'NAME': 'N'}

{'CODE': '12GG233'}
PASSED       [100%]
{'CODE': 'N', 'NAME': 'T'}

{'NAME': 'BlvUbOLHjWlqXkSHqkeGumnnhIbrPvuhkxhddTrMVAwaolyCwY'}
```
And never failed because I made requirements to "NAME" - "N" field 

I added it in project "tests" directory

## Getting started

This package is tested with Python 3.9-3.11 and Pypy 3.
There are two ways to install the library:

* Installation using pip (a Python package manager):

```
pip install combidata
```
* Installation from source (requires git):

```
git clone https://github.com/Warrfie/combidata
cd combidata
python setup.py install
```
or:
```
pip install git+https://github.com/Warrfie/combidata
```

It is generally recommended to use the first option.

*Package is still under development, and it has regular updates, do not forget to update it regularly by calling*
```
pip install combidata --upgrade
```