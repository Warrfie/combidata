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

        self.additional_fields = copy.deepcopy(case)  # TODO make normal warehouse
        # TODO add additional checks
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
