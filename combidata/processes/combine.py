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

def join_requirements(a, b):
    left = copy.deepcopy(a)
    right = copy.deepcopy(b)
    for field, mode in left.items():
        if field in right.keys():
            right[field] = mode.intersection(right[field])
        else:
            right.update({field: mode})
    return right

def recu_update_test_seed(init_lib, requirements, test_seed):
    formed_requirements = {field: {mode} if mode is isinstance(mode, set) else mode for field, mode in test_seed.items()}
    if check_join(formed_requirements, requirements):
        env_requirements = copy.deepcopy(requirements)  # for not chosen cases
        for field in list(set(requirements.keys()).intersection(set(formed_requirements.keys()))):
            del env_requirements[field]
        if len(env_requirements.keys()) == 0:
            return formed_requirements
        current_field = list(env_requirements.keys())[0]
        inert_modes = [mode for mode in list(env_requirements[current_field]) if
                       init_lib[current_field][mode].type_of_case is None]
        typed_modes = [mode for mode in list(env_requirements[current_field]) if
                       init_lib[current_field][mode].type_of_case is not None]
        for mode in inert_modes:
            if init_lib[current_field][mode].requirements is None:
                possible_formed_requirements = copy.deepcopy(formed_requirements)
                possible_formed_requirements.update({current_field: {mode}})
                possible_env_requirements = copy.deepcopy(env_requirements)
                if (exp:=recu_update_test_seed(init_lib, possible_env_requirements, possible_formed_requirements)) is not None:
                    return exp
            else:
                mode_requirements = init_lib[current_field][mode].requirements
                if check_join(formed_requirements, mode_requirements) and check_join(env_requirements, mode_requirements):
                    new_requirements = join_requirements(env_requirements, mode_requirements)
                    possible_formed_requirements = copy.deepcopy(formed_requirements)
                    possible_formed_requirements.update({current_field: {mode}})
                    if (exp := recu_update_test_seed(init_lib, new_requirements, possible_formed_requirements)) is not None:
                        return exp
        else:
            for mode in typed_modes:
                if init_lib[current_field][mode].requirements is None:
                    possible_formed_requirements = copy.deepcopy(formed_requirements)
                    possible_formed_requirements.update({current_field: {mode}})
                    possible_env_requirements = copy.deepcopy(env_requirements)
                    if (exp := recu_update_test_seed(init_lib, possible_env_requirements,
                                                possible_formed_requirements)) is not None:
                        return exp
                else:
                    mode_requirements = init_lib[current_field][mode].requirements
                    if check_join(formed_requirements, mode_requirements) and check_join(env_requirements,
                                                                                         mode_requirements):
                        new_requirements = join_requirements(env_requirements, mode_requirements)
                        possible_formed_requirements = copy.deepcopy(formed_requirements)
                        possible_formed_requirements.update({current_field: {mode}})
                        if (exp := recu_update_test_seed(init_lib, new_requirements, possible_formed_requirements)) is not None:
                            return exp
        return None
    return None


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
            if (possible_test_seed := recu_update_test_seed(init_lib, init_lib[field][example_mode].requirements, possible_test_seed)) is not None:
                if (new_test_seed := recu_create_test_seed(init_lib, non_combined_fields[1:], copy.deepcopy(possible_test_seed))) is not None:
                    new_test_seed.update({field: example_mode})
                    return new_test_seed
    return None



def combine(combination):
    combination.test_seed = {combination.main_case.field_name: combination.main_case.field_mode}

    non_combined_fields = list(combination.init_lib.keys())
    del non_combined_fields[non_combined_fields.index(combination.main_case.field_name)]
    random.shuffle(non_combined_fields)

    if combination.main_case.requirements is not None:
        assert recu_update_test_seed(combination.init_lib, combination.main_case.requirements, combination.test_seed), "Can't combine!"

    if (new_test_seed := recu_create_test_seed(combination.init_lib, list(non_combined_fields), copy.deepcopy(combination.test_seed))) is None:
        raise "Can't combine!"
    else:
        combination.test_seed.update(new_test_seed)



    combination.other_cases = {field: combination.init_lib[field][mode] for field, mode in combination.test_seed.items() if field != combination.main_case.field_name}

    return True

