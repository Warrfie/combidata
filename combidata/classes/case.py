import copy


class Case:
    field_name = None
    field_mode = None

    value = None
    case_name = None

    is_presented = True

    gen_func = None
    type_of_case = None
    requirements = None
    options = None

    def __init__(self, case: dict, field_name, field_mode):

        self.additional_fields = copy.deepcopy(case)  # TODO make normal warehouse

        self.field_name = field_name
        self.field_mode = field_mode
        self.case_name = case["name"]



        self.value = None if "value" not in case.keys() else case["value"]

        self.type_of_case = None if "type" not in case.keys() else case["type"]

        self.gen_func = None if "gen_func" not in case.keys() else case["gen_func"]

        self.is_presented = True if "is_presented" not in case.keys() else case["is_presented"]

        if "requirements" not in case.keys():
            self.requirements = None
        else:
            self.hand_requirements(case["requirements"])

        self.options = None if "options" not in case.keys() else case["options"]





    def hand_requirements(self, requirements):
        if isinstance(requirements, dict):
            self.requirements = copy.deepcopy(requirements)
            for field, mode in self.requirements.items():
                if isinstance(mode, list):
                    self.requirements[field] = set(mode)
                elif isinstance(mode, str):
                    self.requirements[field] = {mode}
                else:
                    raise f"In case '{self.case_name}' requirements modes is not set or list instance"
        else:
            raise f"In case '{self.case_name}' requirements is not dict instance"
