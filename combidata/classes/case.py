import copy


class Case:
    """
    Presents one variation of field

    field_name: holds name of field. In initial lib - hashable key that holds cases (str)

    field_mode: holds case mode (short name). In initial lib - hashable key that holds case (str)

    case_name: holds case full name. Key "name" in initial lib (str)

    gen_func: holds function for generation. By default, takes only one argument if you use options,
    can take more. Key "gen_func" in initial lib (function)

    value: holds case value. It will be first argument of gen_func if gen_func in case else it will be result.
    Key "value" in initial lib (anything)

    options: holds functions and another stuff which will unpack into gen_func. "combination" is reserved string.
    Key "options" in initial lib (dictionary)

    is_presented: holds flag for export function. It will be not exported if False.
    Key "is_presented" in initial lib (boolean)

    requirements: holds possible modes of another fields. Key "requirements" in initial lib (dictionary)

    type: Generator will choose that case like main case when you will run test of that type.
    Key "type" in initial lib (string)

    """

    def __init__(self, case: dict, field_name: str, field_mode: str):
        # TODO add additional checks
        self.field_name = field_name
        self.field_mode = field_mode
        self.case_name = case["name"]

        self.value = case.get("value", None)
        self.type_of_case = case.get("type", None)
        self.gen_func = case.get("gen_func", None)
        self.is_presented = case.get("is_presented", True)
        self.options = case.get("options", None)

        if "requirements" not in case.keys():
            self.requirements = None
        else:
            self.hand_requirements(case["requirements"])

        self.additional_fields = self.form_additional_fields(case)



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

    def form_additional_fields(self, case):
        keys_list = ["name", "value", "type", "gen_func", "is_presented", "options", "requirements"]
        return copy.deepcopy({key: value for key, value in case.items() if key not in keys_list})
