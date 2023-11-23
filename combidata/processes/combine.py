from combidata.classes.mul_dim_graph import MDG


def combine(combination):
    neutral_lib = combination.init_lib

    combi_graph = MDG(neutral_lib, combination.types_for_generation, combination.logger, combination.generator_id)

    main_case = combination.main_case

    combination.test_seed = combi_graph.seed(main_case)

    combination.other_cases = {field: combination.init_lib[field][mode] for field, mode in combination.test_seed.items()
                               if field != combination.main_case.field_name}

    if combination.logger:
        combination.logger.add_log(combination.generator_id,
                                   f"Generated seed: {str(combination.test_seed)}")

    return True
