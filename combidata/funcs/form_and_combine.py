import copy
import random
from combidata.classes.combination import current_workflow

def should_keep(x):
    return len(x) > 1


def form_template(lib):
    template = {}
    for field, modes in lib.items():
        template[field] = {}
        for mode in modes:
            template[field][mode] = copy.deepcopy(
                lib[field][mode])  # TODO fix_it copy.deepcopy(lib[field][mode]) is to dum
            for seed_field, seed_modes in lib.items():
                if seed_field != field:
                    template[field][mode].requirements[seed_field] = set(seed_modes)
    return template


def can_combine(neutral_lib, current_case, types_for_generation):
    case = copy.deepcopy(current_case)
    if case.field_name not in neutral_lib.keys() or not neutral_lib[case.field_name].get(case.field_mode, False):
        return False
    case.requirements = neutral_lib[case.field_name][case.field_mode].requirements
    copied_lib = copy.deepcopy(neutral_lib)

    for mode in neutral_lib[case.field_name].keys():
        if mode != case.field_mode:
            del copied_lib[case.field_name][mode]

    for field, modes in neutral_lib.items():
        if field != case.field_name:
            for mode in neutral_lib[field].keys():
                if mode not in case.requirements[field]:
                    del copied_lib[field][mode]

    modes_count = 0

    for modes in copied_lib.values():
        if not modes:
            return False
        modes_count += len(modes)

    if modes_count == len(copied_lib.keys()):
        for field, modes in copied_lib.items():
            for case in modes.values():
                for case_field, case_modes in case.requirements.items():
                    if not list(copied_lib[case_field].keys())[0] in case_modes:
                        return False
        return copied_lib
    else:
        fields = [list(mode.values()) for mode in copied_lib.values()]
        random.shuffle(fields)
        fields = list(filter(should_keep, fields))
        cases = fields[0]
        random.shuffle(cases)
        for case in cases:
            if case.type_of_case in types_for_generation and (result := can_combine(copied_lib, case, types_for_generation)):
                return result
        else:
            return False


def unlimited_cases(init_lib, cases_lib, workflow, types_for_generation):
    correct_cases = {}
    is_full = False
    current_keys_list = []
    counter = 0

    workflow = copy.deepcopy(workflow)
    must_prove = "ST_COMBINE" in [process.name for process in current_workflow(workflow, True)]

    if not must_prove:
        correct_cases = copy.deepcopy(cases_lib)
        is_full = True
        current_keys_list = list(correct_cases.keys())
        random.shuffle(current_keys_list)

    while True:
        if is_full:
            if current_keys_list:
                combination_name = current_keys_list.pop()
                if counter == 0:
                    yield {combination_name: cases_lib[combination_name]}
                else:
                    yield {f"{combination_name} [{counter}]": cases_lib[combination_name]}
            else:
                current_keys_list = list(correct_cases.keys())
                random.shuffle(current_keys_list)
                counter += 1
                combination_name = current_keys_list.pop()
                yield {f"{combination_name} [{counter}]": cases_lib[combination_name]}
        else:
            from combidata.classes.mul_dim_graph import MDG
            combi_graph = MDG(init_lib, types_for_generation)  # todo add logger
            combinations = list(cases_lib.keys())
            random.shuffle(combinations)
            for combination_name in combinations:
                main_case = cases_lib[combination_name].main_case
                if main_case.field_name in combi_graph.neutral_lib.keys() and main_case.field_mode in \
                        combi_graph.neutral_lib[main_case.field_name].keys() and combi_graph.can_combine(main_case):
                    correct_cases.update({combination_name: main_case})
                    yield {combination_name: cases_lib[combination_name]}
                is_full = True
                current_keys_list = list(correct_cases.keys())
                random.shuffle(current_keys_list)
                counter += 1