[![PyPi Package Version](https://img.shields.io/pypi/v/combidata.svg)](https://pypi.python.org/pypi/combidata)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/combidata.svg)](https://pypi.python.org/pypi/combidata)
[![PyPi status](https://img.shields.io/pypi/status/combidata.svg?style=flat-square)](https://pypi.python.org/pypi/combidata)

# <p align="center">Combidata

Combidata is a flexible and powerful Python library designed for generating various combinations of test data based on defined cases and rules. 
It is especially useful for testing, debugging, and analyzing software applications and systems.


The core functionality of the Combidata library is provided by the `DataGenerator` class, which takes in test flags and a dictionary containing all cases, forms, and workflows. 
The `DataGenerator` creates `Combination` instances from the possible cases. 
The `run` function in each `Combination` instance processes all steps in the specified workflow.

## New features
0.2.0:
1) Ok, now its Beta ;)
2) Fixed combination bug

0.1.9:
1) Now you can use 'types_for_generation' in initialisation of 'DataGenerator'

0.1.8:
1) Now you can use multiply symbols modes
2) Generate any number of data combinations, even if there are only a few cases.
3) Use the `get_one()` function in the `DataGenerator` class for generating a single Combination object.

## Structure of input library

```python
library = {
            "cases": {},
            "workflow": (ST_COMBINE, ST_GENERATE, ST_FORM),
            "tools": {},
            "template": {}
}
```
The `cases` key contains a library instance with all your defined cases. 

The `workflow` key stores a list of tuple or one tuple of processes to be executed. 
If you use list, every `run()` function will process all steps in the current tuple

The `tools` key holds a dictionary with items that can be utilized within the processes. 

Finally, the `template` key contains a template used for exporting the results.


## Cases

Cases structure hold fields names as keys and every field name holds field cases codes as a keys
and every field cases codes holds case structure. 
I know, very complicate, but example will help you:

```python
library["cases"]["NAME"] = {
        "True": {
            "gen_func": re_generate,
            "value": r"[a-zA-Z]{50}",
            "name": "Standart NAME check"
        },
        "False": {
            "value": "12345",
            "type": "error",
            "name": "Check NAME with error"
        },
        "None": {
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

## Workflow

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

## Tools
Just warehouse for items, funcs or other stuff that you can use in steps or generators via .tools
```python
"tools": {
    "UTILS": utilites,
    "TOKEN": token_generator
}

#....

block = combination.tools["UTILS"].get_block()

```

## Template
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

## Example

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

## Installation

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

## Contributing
Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest new features through the GitHub repository. We appreciate your help in improving Combidata!

## License
Combidata is released under the MIT License. See the LICENSE file for more details.

## Support
If you need help with Combidata or have any questions, please open an issue on GitHub or contact the maintainers directly 

Telegram — https://t.me/sasisochka

Linkedin — https://www.linkedin.com/in/yasasisochka/


## Acknowledgments
A special thanks to the community for their support, contributions, and valuable feedback. Your input helps make Combidata a better tool for everyone!

With Combidata, you can easily generate test data for your applications and systems, ensuring that they are robust and reliable under various conditions. Start using Combidata today to improve the quality of your testing and development process!