import copy
import random

from combidata.classes.case import Case
from combidata.classes.combination import Combination, current_workflow
from combidata.classes.mul_dim_graph import MDG
from combidata.funcs.exeptions import CombinatoricsError
from combidata.funcs.form_and_combine import unlimited_cases


def check_all_names(init_lib):
    name_set = set()
    not_unic_items = ""
    for field_name, cases in init_lib["cases"].items():
        for case_code, case in cases.items():
            if case["name"] in name_set:
                not_unic_items += f"Case [{case_code}] for [{field_name}] have not unique name: {case['name']}\n"
            name_set.add(case["name"])

    if not_unic_items:
        raise ValueError(not_unic_items)


def check_input_data(amount, banned_fields, possible_fields, library, logger, generator_id):
    if not (amount is None or (isinstance(amount, int) and amount > 0)):
        raise ValueError("Amount must be an integer greater than 0")

    if not (banned_fields is None or isinstance(banned_fields, list)):
        raise TypeError("Banned_fields must be a list instance")

    if not (possible_fields is None or isinstance(possible_fields, list)):
        raise TypeError("Possible_fields must be a list instance")

    if banned_fields is not None and possible_fields is not None:
        raise ValueError("You can't use banned_fields and possible_fields arguments simultaneously")

    if not ((logger and generator_id) or logger is None):
        raise ValueError("You must use both logger and generator_id, or neither")

    check_all_names(library)


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

        check_input_data(amount, banned_fields, possible_fields, library, logger, generator_id)

        self.modes_for_gen = self.form_modes_for_gen(possible_modes)
        self.init_lib = self.form_init_lib(library)
        self.dell_fields(possible_fields, banned_fields)
        self.template = library.get("template")
        self.tools = library.get("tools")
        self.logger = logger
        self.generator_id = generator_id

        self.type_of_cases = type_of_cases if type_of_cases else "standard"
        self.workflow = self.get_workflow(library["workflow"], type_of_cases)

        if types_for_generation is None:
            types_for_generation = ["standard"]
        if not isinstance(types_for_generation, list):
            types_for_generation = [types_for_generation]
        self.types_for_generation = types_for_generation

        self.form_combinations()

        assert self.combinations, "No combinations for tests"  # TODO deep logging needed

        if amount:
            self.extend_cases(amount)

    def extend_cases(self, amount):
        temp = {}
        for test_case in unlimited_cases(self.init_lib, self.combinations, self.workflow, self.types_for_generation):
            if amount != 0:
                temp.update(test_case)
                amount -= 1
            else:
                self.combinations = temp
                return

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
                del self.combinations[combination_name]  # todo logs!

    def run_one(self):
        combinations = list(self.combinations.keys())
        random.shuffle(combinations)
        for combination_name in combinations:
            combinations[combination_name].run()
            if combinations[combination_name].step_done != CombinatoricsError():
                return combinations[combination_name]

    def get_one(self):
        for test_case in unlimited_cases(self.init_lib, self.combinations, self.workflow, self.types_for_generation):
            return test_case[list(test_case.keys())[0]]  # todo ugly

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
