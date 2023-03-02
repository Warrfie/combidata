import random

from combidata.classes.case import Case
from combidata.classes.combination import Combination, step_not_done


class DataGenerator:
    """
    Input

    library: Main library with all cases and main info (dict)

    banned_fields: What fields can't be combined

    possible_fields: What fields can be combined

    possible_modes: What modes can be combined

    type_of_cases: What types will be main cases

    amount: amount of tests

    Stored

    combinations: dictionary with main full case name as a key and Combination items (dict)

    init_lib: handled copy of main library (dict)

    template: holds export template (dict)

    tools: holds dictionary with items which can be used in processes (dict)

    workflow: holds list or tuple with processes

    """

    def __init__(self, library: dict, banned_fields: None | list = None, possible_fields: None | list = None,
                 possible_modes: None | dict = None, type_of_cases: None | str = None, amount: int = None):
        assert banned_fields is None or isinstance(banned_fields, list), "banned_fields must be list instance"
        assert possible_fields is None or isinstance(possible_fields, list), "possible_fields must be list instance"
        assert banned_fields is None or possible_fields is None, "You can't use banned_fields and possible_fields arguments simultaneously"

        self.combinations = {}

        self.init_lib = {}
        for field_name, field in library["cases"].items():
            self.init_lib[field_name] = {}
            for field_mode, case in field.items():
                self.init_lib[field_name].update({field_mode: Case(case, field_name, field_mode)})
                if possible_modes is not None and field_name in possible_modes.keys() and field_mode not in \
                        possible_modes[field_name]:
                    self.init_lib[field_name][field_mode].type_of_case = "OFF"

        if possible_fields is not None or banned_fields is not None:
            banned_fields = banned_fields if possible_fields is None else [field for field in self.init_lib.keys() if
                                                                           field not in possible_fields]
            for field in banned_fields:
                del self.init_lib[field]

        self.template = library["template"]
        self.tools = library["tools"]
        if isinstance(library["workflow"], dict):
            if type_of_cases in library["workflow"].keys():
                self.workflow = library["workflow"][type_of_cases]
            else:
                self.workflow = library["workflow"]["standard"]
        else:
            self.workflow = library["workflow"]
        # TODO for next realises — make more consistency checks

        for field_name, cases in self.init_lib.items():
            for field_mode, case in cases.items():
                if case.type_of_case == type_of_cases:
                    assert case.case_name not in self.combinations.keys(), case.case_name + " - is not unique"
                    self.combinations.update({case.case_name: Combination(case, self.workflow, self.init_lib,
                                                                          self.template, self.tools)})

        if amount is not None:  # TODO for next realises — upgrade that algorithm
            if amount >= len(self.combinations.keys()):
                return  # TODO for next realises — make additional cases
            for _ in range(len(self.combinations.keys()) - amount):
                del self.combinations[random.choice(list(self.combinations.keys()))]

    def run(self):
        workflow = self.workflow.pop(0) if isinstance(self.workflow, list) else self.workflow

        for current_step in workflow:
            while step_not_done(current_step.name, list(self.combinations.values())):
                for combination in self.combinations.values():
                    if combination.step_done != current_step.name:
                        current_step.activate(combination)
