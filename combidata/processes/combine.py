import copy
import random


def crop_types(current_dict, poss_types):
    for unit, modes in current_dict.items():
        for mode in list(modes.keys()):
            if current_dict[unit][mode].type_of_case not in poss_types:
                del current_dict[unit][mode]


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

def form_poss(init_lib, neutral_types=None):
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
                        modes_for_hunt = set(neutral_lib[req_unit].keys()) - req_modes
                        for target_mode in modes_for_hunt:
                            neutral_lib[req_unit][target_mode].requirements[field] = \
                                neutral_lib[req_unit][target_mode].requirements[field] - set(mode)
                            if not neutral_lib[req_unit][target_mode].requirements[field]:
                                del neutral_lib[req_unit][target_mode]

    if neutral_types is not None:
        crop_types(neutral_lib, neutral_types)

    return neutral_lib


def process_mode(seed, poss_di, chosen_unit, chosen_mode):
    for pos_unit, pos_modes in poss_di[chosen_unit][chosen_mode].requirements.items():
        if poss_di.get(pos_unit):
            modes_for_del = set(poss_di[pos_unit].keys()) - set(pos_modes)
            for mode_for_del in modes_for_del:
                del poss_di[pos_unit][mode_for_del]
    seed[chosen_unit] = chosen_mode
    del poss_di[chosen_unit]
    return form_poss(poss_di)

def generate_seed(di, main_unit, main_mode):
    poss_di = copy.deepcopy(di)
    seed = {}

    poss_di = process_mode(seed, poss_di, main_unit, main_mode)

    while poss_di:
        chosen_unit = random.choice(list(poss_di.keys()))
        chosen_mode = random.choice(list(poss_di[chosen_unit].keys()))
        poss_di = process_mode(seed, poss_di, chosen_unit, chosen_mode)

    return seed

def combine(combination):
    neutral_lib = combination.init_lib
    main_case = combination.main_case

    combination.test_seed = generate_seed(neutral_lib, main_case.field_name, main_case.field_mode)

    combination.other_cases = {field: combination.init_lib[field][mode] for field, mode in combination.test_seed.items()
                               if field != combination.main_case.field_name}

    return True
