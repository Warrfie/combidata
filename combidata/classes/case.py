import copy


class Case:
    """
    Represents a specific variation or scenario for a given field.

    Attributes:

    - field_name (str): Name of the field. Serves as a unique identifier
      for the field.

    - field_mode (str): Concise identifier for the case mode. Provides a
      quick reference to the type or mode of the case.

    - case_name (str): Full descriptive name of the case.

    - gen_func (function): Function for generating data/values for the case.
      Accepts 'value' as its default argument. If additional options are
      provided, they can be unpacked into this function.

    - value (any): Primary value for the case. Used as the result if no
      gen_func is defined, otherwise passed as the first argument to gen_func.

    - options (dict): Additional parameters for gen_func. "combination" is
      a reserved key.

    - is_presented (bool): Flag indicating if the case should be exported.
      If False, the case is excluded from exports.

    - requirements (dict): Permissible modes for related fields. Ensures
      valid combinations during testing.

    - type (str): Primary category or type of test this case pertains to.

    - additional_fields (dict): Additional attributes or properties associated
      with the case.This provides flexibility for extending the functionality
      or storing extra metadata related to the case.

    Notes:
    Attributes and roles are based on the initial library's design.
    """

    def __init__(self, case: dict, field_name: str, field_mode: str):
        # TODO add additional checks
        self.field_name = field_name
        self.field_mode = field_mode
        self.case_name = case["name"]

        self.value = case.get("value", None)
        self.type_of_case = case.get("type", "standard")
        self.gen_func = case.get("gen_func", None)
        self.is_presented = case.get("is_presented", True)
        self.options = case.get("options", None)

        if "requirements" not in case.keys():
            self.requirements = {}
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
