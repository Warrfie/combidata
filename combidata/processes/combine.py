import copy
import random


def check_join(main, rule):
    if rule is None:
        return False

    for field, mode in rule.items():
        if field in main.keys():
            if len(mode.intersection(main[field])) == 0:
                return False
    return True


def form_requirements(init_lib, rule, test_seed):
    exp = copy.deepcopy(rule)
    for field, mode_set in rule.items():
        mode_list = list(mode_set)
        while len(mode_list) > 0:
            mode = random.choice(mode_list)
            del mode_list[mode_list.index(mode)]  # TODO beautify

            if init_lib[field][mode].requirements is not None:
                new_rule = form_requirements(init_lib, init_lib[field][mode].requirements, test_seed)
                if check_join(exp, new_rule):
                    possible_requirements = copy.deepcopy(exp)
                    possible_requirements.update(new_rule)
                    if check_join(test_seed, possible_requirements):
                        exp = possible_requirements
                        break
                    elif len(mode_list) == 0:
                        return None
                elif len(mode_list) == 0:
                    return None
            else:
                if check_join(exp, {field: {mode}}):
                    possible_requirements = copy.deepcopy(exp)
                    possible_requirements.update({field: {mode}})
                    if check_join(test_seed, possible_requirements):
                        exp = possible_requirements
                        break
                    elif len(mode_list) == 0:
                        return None
                elif len(mode_list) == 0:
                    return None

    return exp

def update_test_seed(init_lib, requirements, test_seed, non_combined_fields):
    case_requirements = form_requirements(init_lib, requirements, test_seed)
    if check_join(test_seed, case_requirements):
        for field, mode in case_requirements.items():
            if field in non_combined_fields:
                test_seed.update({field: mode.pop()})
                del non_combined_fields[non_combined_fields.index(field)]
    else:
        return False

    return True

def recu_create_test_seed(init_lib, non_combined_fields, test_seed):
    if len(non_combined_fields) == 0:
        return test_seed
    field = non_combined_fields[0]
    cases = init_lib[field]
    field_modes = [case.field_mode for case in cases.values() if case.type_of_case is None]
    random.shuffle(field_modes)
    for example_mode in field_modes:
        if cases[example_mode].requirements is None:
            if (new_test_seed := recu_create_test_seed(init_lib, non_combined_fields[1:], copy.deepcopy(test_seed))) is not None:
                new_test_seed.update({field: example_mode})
                return new_test_seed
        else:
            possible_test_seed = copy.deepcopy(test_seed)
            if update_test_seed(init_lib, init_lib[field][example_mode].requirements, possible_test_seed, non_combined_fields[1:]):
                if (new_test_seed := recu_create_test_seed(init_lib, non_combined_fields[1:], copy.deepcopy(possible_test_seed))) is not None:
                    new_test_seed.update({field: example_mode})
                    return new_test_seed
    return None

def create_test_seed(init_lib, non_combined_fields, test_seed):
    fields_and_modes_for_combine = {field: [mode for mode in init_lib[field].keys() if init_lib[field][mode].type_of_case is None] for field in non_combined_fields}
    env_pass = [{non_combined_fields[0]: fields_and_modes_for_combine[non_combined_fields[0]][0]}]
    env_seed = [{"INIT": test_seed}]
    while True:
        current_combined_fields = [list(field_param.keys())[0] for field_param in env_pass]
        current_seed = list(env_seed[-1].values())[0]
        available_fields = [field for field in non_combined_fields if (field not in current_seed.keys() and field not in current_combined_fields)]
        if len(available_fields) > 0:
            current_field = available_fields[0]
            for current_mode in fields_and_modes_for_combine[current_field]:
                if init_lib[current_field][current_mode].requirements is None:
                    env_pass.append({current_field: current_mode})
                    break
                else:
                    possible_test_seed = copy.deepcopy(current_seed)
                    if update_test_seed(init_lib, init_lib[current_field][current_mode].requirements, possible_test_seed, available_fields[1:]):
                        env_pass.append({current_field: current_mode})
                        env_seed.append({current_field: possible_test_seed})
                        break
            else:
                while True:
                    current_field = list(env_pass[-1].keys())[0]
                    not_correct_mode = list(env_pass[-1].values())[0]
                    if current_field in env_seed[-1].keys():
                        del env_seed[-1]
                    current_seed = list(env_seed[-1].values())[0]
                    for current_mode in fields_and_modes_for_combine[current_field][fields_and_modes_for_combine[current_field].index(not_correct_mode) + 1:]:
                        if init_lib[current_field][current_mode].requirements is None:
                            env_pass.append({current_field: current_mode})
                            break
                        else:
                            possible_test_seed = copy.deepcopy(current_seed)
                            if update_test_seed(init_lib, init_lib[current_field][current_mode].requirements,
                                                possible_test_seed, available_fields[1:]):
                                env_pass.append({current_field: current_mode})
                                env_seed.append({current_field: possible_test_seed})
                                break
                    else:
                        del env_pass[-1]
        else:
            combined_seed = {list(field_mode.keys())[0]: list(field_mode.values())[0] for field_mode in env_pass}
            combined_seed.update(list(env_seed[-1].values())[0])
            return combined_seed





def combine(combination):
    combination.test_seed = {combination.main_case.field_name: combination.main_case.field_mode}

    non_combined_fields = list(combination.init_lib.keys())
    del non_combined_fields[non_combined_fields.index(combination.main_case.field_name)]
    random.shuffle(non_combined_fields)

    if combination.main_case.requirements is not None:
        assert update_test_seed(combination.init_lib, combination.main_case.requirements, combination.test_seed, non_combined_fields), "Can't combine!"

    if (new_test_seed := create_test_seed(combination.init_lib, list(non_combined_fields), copy.deepcopy(combination.test_seed))) is None:
        raise "Can't combine!"
    else:
        combination.test_seed.update(new_test_seed)



    combination.other_cases = {field: combination.init_lib[field][mode] for field, mode in combination.test_seed.items() if field != combination.main_case.field_name}

    return True

