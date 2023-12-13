def find_replace_in_dict(template, generated_data, keys):
    result = {}
    for key, value in template.items():
        if isinstance(value, dict):
            result.update({key: find_replace_in_dict(value, generated_data, keys)})
        elif isinstance(value, str) and value in keys:
            if value in generated_data.keys():
                result.update({key: generated_data[value]})
        else:
            result.update({key: value})

    return result

def form(combination):
    combination.formed_data = find_replace_in_dict(combination.template, combination.generated_data, combination.init_lib.keys())

    if combination.logger:
        combination.logger.add_log(combination.generator_id,
                                   f"Formed data: {str(combination.formed_data)}")

    return True