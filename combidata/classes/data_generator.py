import copy
import random

from combidata.classes.case import Case
from combidata.classes.combination import Combination, step_not_done


def extend_dict(input_dict, final_key_count):
    output_dict = {}
    dict_keys = list(input_dict.keys())
    key_count = len(dict_keys)

    i = 0
    added_key_count = 0
    shuffle_point = 0 if key_count > final_key_count else (final_key_count // key_count) * key_count

    while added_key_count < final_key_count:
        if i % key_count == 0 and i == shuffle_point:
            random.shuffle(dict_keys)
        key = dict_keys[i % key_count]
        value = input_dict[key]

        if i < key_count:
            output_dict[key] = copy.deepcopy(value)
        else:
            extended_key = f"{key}[{i // key_count}]"
            output_dict[extended_key] = copy.deepcopy(value)

        i += 1
        added_key_count += 1

    return output_dict


class DataGenerator:
    """
    Input

    library: Main library with all cases and main info (dict)

    banned_fields: What fields can't be combined

    possible_fields: What fields can be combined

    possible_modes: What modes can be combined

    type_of_cases: What types will be main cases

    types_for_generation: What types will be chosen as standard cases

    amount: amount of tests

    Stored

    combinations: dictionary with main full case name as a key and Combination items (dict)

    init_lib: handled copy of main library (dict)

    template: holds export template (dict)

    tools: holds dictionary with items which can be used in processes (dict)

    workflow: holds list or tuple with processes

    """

    def __init__(self, library: dict,
                 banned_fields: None | list = None,
                 possible_fields: None | list = None,
                 possible_modes: None | dict = None,
                 type_of_cases: None | str = None,
                 types_for_generation: None | str | list = None,
                 amount: int = None):
        assert amount is None or (isinstance(amount, int) and amount > 0), "amount must be integer > 0"
        assert banned_fields is None or isinstance(banned_fields, list), "banned_fields must be list instance"
        assert possible_fields is None or isinstance(possible_fields, list), "possible_fields must be list instance"
        assert banned_fields is None or possible_fields is None, "You can't use banned_fields and possible_fields arguments simultaneously"

        modes_for_gen = copy.deepcopy(possible_modes)

        if modes_for_gen is not None:
            for key, value in modes_for_gen.items():
                if isinstance(value, str):
                    modes_for_gen[key] = [value]



        self.init_lib = {}
        for field_name, field in library["cases"].items():
            self.init_lib[field_name] = {}
            for field_mode, case in field.items():
                self.init_lib[field_name].update(
                    {field_mode: (case if isinstance(case, Case) else Case(case, field_name, field_mode))})
                if modes_for_gen is not None:
                    if field_name in modes_for_gen.keys() and field_mode not in modes_for_gen[field_name]:
                        self.init_lib[field_name][field_mode].type_of_case = "OFF"
                    elif requirements := self.init_lib[field_name][field_mode].requirements:
                        for rec_field, rec_modes in requirements.items():
                            if rec_field in modes_for_gen.keys() and not rec_modes & set(modes_for_gen[rec_field]):
                                self.init_lib[field_name][field_mode].type_of_case = "OFF"
                                break

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

        copy_of_init_lib = copy.deepcopy(self.init_lib)
        if not isinstance(types_for_generation, list):
            types_for_generation = [types_for_generation]
        for field_name, field in copy_of_init_lib.items():
            for field_mode, case in field.items():
                case.type_of_case = None if case.type_of_case in types_for_generation else "OFF"

        self.combinations = {}
        for field_name, cases in self.init_lib.items():
            for field_mode, case in cases.items():
                if case.type_of_case == type_of_cases:
                    assert case.case_name not in self.combinations.keys(), case.case_name + " - is not unique"
                    self.combinations.update({case.case_name: Combination(case, self.workflow, copy_of_init_lib,
                                                                          self.template, self.tools)})

        if amount is not None:
            self.combinations = extend_dict(self.combinations, amount)

    def run(self):  # todo make STOP
        workflow = self.workflow.pop(0) if isinstance(self.workflow, list) else self.workflow
        combinations = list(self.combinations.values())

        for current_step in workflow:
            while step_not_done(current_step.name, combinations):
                for combination in combinations:
                    if combination.step_done != current_step.name:
                        current_step.activate(combination)

    def get_one(self):
        return self.combinations[random.choice(list(self.combinations.keys()))]
