def step_not_done(current_step_name, combi):
    if isinstance(combi, list):
        for combination in combi:
            if combination.step_done != current_step_name or combination.step_done == "STOP":
                return True
    else:
        if combi.step_done != current_step_name or combi.step_done == "STOP":
            return True
    return False

class Combination:
    format_func = None
    export_func = None

    test_seed = None
    formed_data = None

    first_comb_func = None
    first_gen_func = None
    uni_export_format = None
    answer = None
    uni_prove = None
    uni_result_format = None

    cache = None
    dev_log = None
    prod_log = None

    step_done = None  # last passed step

    def __init__(self, case, workflow, init_lib, template, tools, type_of_cases=None):
        self.init_lib = init_lib
        self.main_case = case
        self.template = template
        self.tools = tools

        self.generated_data = {}
        self.other_cases = {}

        self.cache = {}

        self.type_of_cases = type_of_cases

        self.workflow = workflow

    def run(self):
        self.workflow = list(self.workflow) if isinstance(self.workflow, list) else self.workflow #todo beautify
        workflow = self.workflow.pop(0) if isinstance(self.workflow, list) else self.workflow
        for current_step in workflow:
            while step_not_done(current_step.name, self):
                if self.step_done != current_step.name:
                    current_step.activate(self)