import copy

from combidata.funcs.exeptions import CombinatoricsError
from combidata.funcs.form_and_combine import form_template, can_combine


def should_keep(x):
    return len(x) > 1


def form_seed(gen_lib):
    return {field: list(modes.keys())[0] for field, modes in gen_lib.items()}


class MDG:
    def __init__(self, init_lib, types_for_generation=None, logger=None, generator_id=None):

        self.init_lib = copy.deepcopy(init_lib)
        self.types_for_generation = types_for_generation
        self.logger = logger
        self.generator_id = generator_id
        self.neutral_lib = self.form_neutral_lib()

    def seed(self, main_case):
        if result := can_combine(self.neutral_lib, main_case, self.types_for_generation):
            return form_seed(result)
        else:
            raise CombinatoricsError()

    def can_combine(self, main_case):
        if can_combine(self.neutral_lib, main_case, self.types_for_generation):
            return True
        else:
            return False

    def form_neutral_lib(self):
        template = form_template(self.init_lib)

        for field, modes in self.init_lib.items():
            for mode in modes:
                if self.init_lib[field][mode].requirements:
                    for req_unit, req_modes in self.init_lib[field][mode].requirements.items():
                        if req_unit in template.keys() and mode in template[field].keys():
                            template[field][mode].requirements[req_unit] = req_modes & \
                                                                           template[field][mode].requirements[
                                                                               req_unit]
                            if not template[field][mode].requirements[req_unit]:
                                del template[field][mode]
                                if self.logger:
                                    self.logger.add_log(self.generator_id,
                                                        f"Mode: {mode} in field: {field}: Was deleted because will never use in generation")
                            modes_for_hunt = set(template[req_unit].keys()) - template[field][mode].requirements[req_unit]
                            for target_mode in modes_for_hunt:
                                template[req_unit][target_mode].requirements[field] = \
                                    template[req_unit][target_mode].requirements[field] - {mode}
                                if not template[req_unit][target_mode].requirements[field]:
                                    del template[req_unit][target_mode]
                                    if self.logger:
                                        self.logger.add_log(self.generator_id,
                                                            f"Mode: {target_mode} in field: {req_unit}: Was deleted because will never use in generation")

        return template
