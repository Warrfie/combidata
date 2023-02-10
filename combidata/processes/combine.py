import copy
import random

def check_join(main, rule):
    for field, mode in rule.items():
        if field in main.keys():
            if mode != main[field]:
                return False
    return True

def form_requirements(init_lib, rule):#todo add [] list choise
    exp = copy.deepcopy(rule)
    for field, mode in rule.items():
        if init_lib[field][mode].requirements is not None:
            new_rule = form_requirements(init_lib, init_lib[field][mode].requirements)
            if check_join(exp, new_rule):
                exp.update(new_rule)
    return exp

def combine(combination):
    combination.test_seed = {combination.main_case.field_name: combination.main_case.field_mode}
    all_fields = list(combination.init_lib.keys())

    if combination.main_case.requirements is not None:
        case_requirements = form_requirements(combination.init_lib, combination.main_case.requirements)
        if check_join(combination.test_seed, case_requirements):
            for name, mode in case_requirements.items():
                if combination.main_case.field_name != name and name in all_fields:
                    combination.other_cases.update({name: combination.init_lib[name][mode]})
                    combination.test_seed.update({name: mode})
                    del all_fields[all_fields.index(name)]


    del all_fields[all_fields.index(combination.main_case.field_name)]

    while len(all_fields) > 0:
        field_name = random.choice(all_fields)
        cases = combination.init_lib[field_name]
        field_modes = [case.field_mode for case in cases.values() if case.type_of_case is None]
        field_mode = None
        for _ in range(len(field_modes)):
            example_mode = random.choice(field_modes)
            if cases[example_mode].requirements is None:
                field_mode = example_mode
                break
            case_requirements = form_requirements(combination.init_lib, cases[example_mode].requirements)
            if check_join(combination.test_seed, case_requirements):
                for name, mode in case_requirements.items():
                    if combination.main_case.field_name != name and name in all_fields:
                        combination.other_cases.update({name: combination.init_lib[name][mode]})
                        combination.test_seed.update({name: mode})
                        del all_fields[all_fields.index(name)]
                field_mode = example_mode
                break
            del field_modes[field_modes.index(example_mode)]

        assert field_mode is not None, "Не удалось подобрать кейс!"

        combination.other_cases.update({field_name: cases[field_mode]})
        combination.test_seed.update({field_name: field_mode})
        del all_fields[all_fields.index(field_name)]

    return True