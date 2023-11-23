import copy
import random


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
        for case in fields[0]:
            if case.type_of_case in types_for_generation and (result := can_combine(copied_lib, case, types_for_generation)):
                return result
        else:
            return False
