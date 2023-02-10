import random

from combidata.classes.combination import Combination


def generate_value(all_fields, case, combination: Combination):
    generated_data = combination.generated_data
    test_seed = combination.test_seed
    cases = combination.other_cases

    if case.options is None:
        if case.gen_func is None:
            item_value = case.value
        else:
            item_value = case.gen_func(case.value)
    else:
        options = {}
        for key, field in case.options.items():
            if isinstance(field, str) and field in test_seed.keys():
                if field in generated_data.keys():
                    options.update({key: generated_data[field]})
                else:
                    generate_value(all_fields, cases[field], combination)
                    options.update({key: generated_data[field]})
            elif isinstance(field, str) and field == "combination":
                options.update({key: combination})
            else:
                options.update({key: field})
        item_value = case.gen_func(case.value, **options)

    if case.is_presented:
        generated_data.update({case.field_name: item_value})
    if case in all_fields:
        del all_fields[all_fields.index(case)]

def generate(combination: Combination):
    all_fields = list(combination.other_cases.values())

    generate_value(all_fields, combination.main_case, combination)

    while len(all_fields) > 0:
        case = random.choice(all_fields)
        generate_value(all_fields, case, combination)

    return True