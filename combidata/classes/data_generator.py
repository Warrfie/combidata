import copy
import random
import traceback
from pprint import pprint

from combidata.classes.case import Case
from combidata.classes.combination import Combination, step_not_done


def crop_types(current_dict, poss_types):
    for unit, modes in current_dict.items():
        for mode in list(modes.keys()):
            if current_dict[unit][mode].type_of_case not in poss_types:
                del current_dict[unit][mode]


def can_combine(neutral_lib, case):
    for field, modes in neutral_lib.items():
        for mode in modes.values():
            if (case.field_name in mode.requirements and case.field_mode in mode.requirements[
                case.field_name]) or mode.field_name == case.field_name:
                break
        else:
            return False
    return True


def form_template(lib):
    template = {}
    for field, modes in lib.items():
        template[field] = {}
        for mode in modes:
            template[field][mode] = copy.deepcopy(
                lib[field][mode])  # TODO fix_it copy.deepcopy(lib[field][mode]) is tooo dum
            for seed_field, seed_modes in lib.items():
                if seed_field != field:
                    template[field][mode].requirements[seed_field] = set(seed_modes)
    return template


def check_all_names(init_lib):
    name_set = set()
    for cases in init_lib["cases"].values():
        for case in cases.values():
            assert case["name"] not in name_set, case["name"] + " - is not unique"
            name_set.update(set(case["name"]))


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
                 amount: int = None,
                 logger=None,
                 generator_id: str = None):

        assert amount is None or (isinstance(amount, int) and amount > 0), "amount must be integer > 0"
        assert banned_fields is None or isinstance(banned_fields, list), "banned_fields must be list instance"
        assert possible_fields is None or isinstance(possible_fields, list), "possible_fields must be list instance"
        assert banned_fields is None or possible_fields is None, "You can't use banned_fields and possible_fields arguments simultaneously"
        check_all_names(library)

        self.modes_for_gen = self.form_modes_for_gen(possible_modes)
        self.init_lib = self.form_init_lib(library)
        self.dell_fields(possible_fields, banned_fields)
        self.template = library["template"]
        self.tools = library.get("tools")
        self.logger = logger
        self.generator_id = generator_id

        assert (logger and generator_id) or logger is None, "You must use logger and generator_id"

        self.workflow = self.get_workflow(library["workflow"], type_of_cases)

        type_of_cases = type_of_cases if type_of_cases else "standard"
        if types_for_generation is None:
            types_for_generation = ["standard"]
        if not isinstance(types_for_generation, list):
            types_for_generation = [types_for_generation]
        neutral_lib = self.form_neutral_lib(self.init_lib)
        self.spread_requirements(neutral_lib)
        crop_types(neutral_lib, types_for_generation)

        self.combinations = self.find_combinations(neutral_lib, type_of_cases)

        assert self.combinations, "No combinations for tests" #TODO deep logging needed

        if amount is not None:
            self.combinations = extend_dict(self.combinations, amount)
    def spread_requirements(self, neutral_lib):
        for field, modes in neutral_lib.items():
            for mode, case in modes.items():
                self.init_lib[field][mode].requirements = case.requirements

    def find_combinations(self, neutral_lib, type_of_cases):
        all_combinations = {}
        for field_name, cases in self.init_lib.items():
            for field_mode, case in cases.items():
                if case.type_of_case == type_of_cases and can_combine(neutral_lib, case):
                    current_combination = Combination(case, self.workflow, neutral_lib,
                                                      self.template, self.tools, self.logger, self.generator_id)
                    all_combinations.update({case.case_name: current_combination})
        return all_combinations

    def run(self):
        workflow = self.workflow.pop(0) if isinstance(self.workflow, list) else self.workflow
        combinations = list(self.combinations.values())

        for current_step in workflow:
            while step_not_done(current_step.name, combinations):
                for combination in combinations:
                    if combination.step_done != current_step.name:
                        if self.logger:
                            self.logger.start_step(self.generator_id, current_step.name)
                        try:
                            current_step.activate(combination)
                        except Exception as e:
                            combination.step_done = "STOP"
                            if self.logger:
                                temp_exep = f"An exception occurred: {type(e).__name__}. "
                                temp_exep += f"Error message: {str(e)}. "
                                traceback_list = traceback.extract_tb(e.__traceback__)
                                if traceback_list:
                                    last_traceback = traceback_list[-1]
                                    file_name = last_traceback.filename
                                    line_number = last_traceback.lineno
                                    temp_exep += f"Occurred at: {file_name}:{line_number}. "
                                self.logger.end_step(self.generator_id, temp_exep)
                            else:
                                raise e
                        else:
                            if self.logger:
                                self.logger.end_step(self.generator_id)


    def get_one(self):
        return self.combinations[random.choice(list(self.combinations.keys()))]

    def form_modes_for_gen(self, possible_modes):
        modes_for_gen = copy.deepcopy(possible_modes)

        if modes_for_gen is not None:
            for key, value in modes_for_gen.items():
                if isinstance(value, str):
                    modes_for_gen[key] = [value]

        return modes_for_gen

    def form_init_lib(self, library):
        init_lib = {}
        for field_name, field in library["cases"].items():
            init_lib[field_name] = {}
            for field_mode, case in field.items():
                init_lib[field_name].update(
                    {field_mode: (case if isinstance(case, Case) else Case(case, field_name, field_mode))})
                if self.modes_for_gen is not None:
                    if field_name in self.modes_for_gen.keys() and field_mode not in self.modes_for_gen[field_name]:
                        init_lib[field_name][field_mode].type_of_case = "OFF"
                    elif requirements := init_lib[field_name][field_mode].requirements:
                        for rec_field, rec_modes in requirements.items():
                            if rec_field in self.modes_for_gen.keys() and not rec_modes & set(
                                    self.modes_for_gen[rec_field]):
                                init_lib[field_name][field_mode].type_of_case = "OFF"
                                break
        return init_lib

    def get_workflow(self, workflow, type_of_cases):
        if isinstance(workflow, dict):
            if type_of_cases in workflow.keys():
                return workflow[type_of_cases]
            else:
                return workflow["standard"]
        else:
            return workflow

    def dell_fields(self, possible_fields, banned_fields):
        if possible_fields is not None or banned_fields is not None:
            banned_fields = banned_fields if possible_fields is None else [field for field in self.init_lib.keys() if
                                                                           field not in possible_fields]
            for field in banned_fields:
                del self.init_lib[field]

    def form_neutral_lib(self, init_lib):
        neutral_lib = form_template(init_lib)

        for field, modes in init_lib.items():
            for mode in modes:
                if init_lib[field][mode].requirements:
                    for req_unit, req_modes in init_lib[field][mode].requirements.items():
                        if req_unit in neutral_lib.keys() and mode in neutral_lib[field].keys():
                            neutral_lib[field][mode].requirements[req_unit] = req_modes & \
                                                                              neutral_lib[field][mode].requirements[
                                                                                  req_unit]
                            if not neutral_lib[field][mode].requirements[req_unit]:
                                del neutral_lib[field][mode]
                                if self.logger:
                                    self.logger.add_log(self.generator_id,
                                                        f"Mode: {mode} in field: {field}: Was deleted because will never use in generation")
                            modes_for_hunt = set(neutral_lib[req_unit].keys()) - req_modes
                            for target_mode in modes_for_hunt:
                                neutral_lib[req_unit][target_mode].requirements[field] = \
                                    neutral_lib[req_unit][target_mode].requirements[field] - set(mode)
                                if not neutral_lib[req_unit][target_mode].requirements[field]:
                                    del neutral_lib[req_unit][target_mode]
                                    if self.logger:
                                        self.logger.add_log(self.generator_id,
                                                            f"Mode: {target_mode} in field: {req_unit}: Was deleted because will never use in generation")



        return neutral_lib
