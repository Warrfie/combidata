import copy
import random

from combidata.classes.case import Case
from combidata.classes.combination import Combination, current_workflow
from combidata.classes.mul_dim_graph import MDG
from combidata.funcs.exeptions import CombinatoricsError


def check_all_names(init_lib):
    name_set = set()
    for cases in init_lib["cases"].values():
        for case in cases.values():
            assert case["name"] not in name_set, case["name"] + " - is not unique"
            name_set.add(case["name"])


class DataGenerator:
    """
DataGenerator Class:

Responsible for generating test data based on the provided configurations and library of cases.

    Attributes:

    - library (dict): The primary library containing all test cases and associated information.
    - banned_fields (list): Fields that should not be combined during test generation.
    - possible_fields (list): Fields that are eligible for combination during test generation.
    - possible_modes (dict): Modes that can be combined for test generation.
    - type_of_cases (list or str): Specifies the types that will be used as main cases.
    - types_for_generation (list or str): Types that will be selected as standard cases for test generation.
    - amount (int): The number of tests to be generated.

    Stored Attributes:

    - combinations (dict): A dictionary storing combinations with the main full case name as the key and instances of the Combination class as values.
    - init_lib (dict): A processed copy of the main library.
    - template (dict): Contains the export template for the generated tests.
    - tools (dict): A dictionary of tools and utilities that can be utilized during test processes.
    - workflow (list/tuple): A collection of processes that define the test generation workflow.

Note:
    The DataGenerator class plays a central role in the test generation process, ensuring that tests are created based on the specified criteria and configurations.
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

        self.combinations = None
        assert amount is None or (isinstance(amount, int) and amount > 0), "amount must be integer > 0"
        assert banned_fields is None or isinstance(banned_fields, list), "banned_fields must be list instance"
        assert possible_fields is None or isinstance(possible_fields, list), "possible_fields must be list instance"
        assert banned_fields is None or possible_fields is None, "You can't use banned_fields and possible_fields arguments simultaneously"
        check_all_names(library)

        self.modes_for_gen = self.form_modes_for_gen(possible_modes)
        self.init_lib = self.form_init_lib(library)
        self.dell_fields(possible_fields, banned_fields)
        self.template = library.get("template")
        self.tools = library.get("tools")
        self.logger = logger
        self.generator_id = generator_id

        assert (logger and generator_id) or logger is None, "You must use logger and generator_id"

        self.type_of_cases = type_of_cases if type_of_cases else "standard"
        self.workflow = self.get_workflow(library["workflow"], type_of_cases)

        if types_for_generation is None:
            types_for_generation = ["standard"]
        if not isinstance(types_for_generation, list):
            types_for_generation = [types_for_generation]
        self.types_for_generation = types_for_generation

        self.form_combinations()

        assert self.combinations, "No combinations for tests"  # TODO deep logging needed

        if amount is not None:
            self.extend_cases(amount)

    def extend_cases(self, amount):

        workflow = copy.deepcopy(self.workflow)
        if "ST_COMBINE" in [process.name for process in current_workflow(workflow, True)]:
            combi_graph = MDG(self.init_lib, self.types_for_generation) #todo add logger
            combinations = list(self.combinations.keys())
            random.shuffle(combinations)
            for combination_name in combinations:
                main_case = self.combinations[combination_name].main_case
                if main_case.field_name in combi_graph.neutral_lib.keys() and main_case.field_mode in combi_graph.neutral_lib[main_case.field_name].keys():
                    if not combi_graph.can_combine(main_case):
                        del self.combinations[combination_name]
                else:
                    del self.combinations[combination_name]

        dict_keys = list(self.combinations.keys())
        random.shuffle(dict_keys)
        key_count = len(dict_keys)

        if key_count == amount:
            return
        elif key_count > amount:
            for i in range(key_count - amount):
                del self.combinations[dict_keys[i]]
            return

        i = 0
        added_key_count = 0
        shuffle_point = (amount // key_count) * key_count

        while added_key_count < amount:
            if i % key_count == 0 and i == shuffle_point:
                random.shuffle(dict_keys)
            key = dict_keys[i % key_count]
            value = self.combinations[key]

            if i < key_count:
                self.combinations[key] = copy.deepcopy(value)
            else:
                extended_key = f"{key}[{i // key_count}]"
                self.combinations[extended_key] = copy.deepcopy(value)

            i += 1
            added_key_count += 1

    def form_combinations(self):
        self.combinations = {}
        for field_name, cases in self.init_lib.items():
            for field_mode, case in cases.items():
                if case.type_of_case == self.type_of_cases:
                    current_combination = Combination(case, self.workflow, self.init_lib,
                                                      self.template, self.tools, self.logger, self.generator_id,
                                                      self.types_for_generation)
                    self.combinations.update({case.case_name: current_combination})

    def run(self):
        combinations_names = list(self.combinations.keys())
        for combination_name in combinations_names:
            self.combinations[combination_name].run()
            if isinstance(self.combinations[combination_name].step_done, type(CombinatoricsError())):
                del self.combinations[combination_name]

    def run_one(self):
        combinations = list(self.combinations.keys())
        random.shuffle(combinations)
        for combination_name in combinations:
            combinations[combination_name].run()
            if combinations[combination_name].step_done != CombinatoricsError():
                return combinations[combination_name]

    def get_one(self):
        workflow = copy.deepcopy(self.workflow)
        if "ST_COMBINE" in [process.name for process in current_workflow(workflow, True)]:
            combi_graph = MDG(self.init_lib, self.types_for_generation)
            combinations = list(self.combinations.keys())
            random.shuffle(combinations)
            for combination in combinations:
                if combi_graph.can_combine(self.combinations[combination].main_case):
                    return self.combinations[combination]
        else:
            combinations = list(self.combinations.keys())
            return self.combinations[random.choice(combinations)]

    # todo def any_passed
    @staticmethod
    def form_modes_for_gen(possible_modes):
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

