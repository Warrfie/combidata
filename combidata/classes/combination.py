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
    """
    test_seed: formed in ST_COMBINE process

    formed_data: formed in ST_FORM process


    step_done: last passed step

    init_lib: copy of init lib

    main_case: store for main case instance
    template: holds export template (dict)
    tools: holds dictionary with items which can be used in processes (dict)
    generated_data: holds all data generated in ST_GENERATE step
    other_cases: holds other cases that take part in test
    cache: some store for your steps and processes
    workflow: holds list or tuple with processes

    """
    test_seed = None
    formed_data = None

    step_done = None  # last passed step

    def __init__(self, case, workflow, init_lib, template, tools):
        self.init_lib = init_lib
        self.main_case = case
        self.template = template
        self.tools = tools

        self.generated_data = {}
        self.other_cases = {}

        self.cache = {}

        self.workflow = workflow

    def run(self):
        self.workflow = list(self.workflow) if isinstance(self.workflow, list) else self.workflow  # todo beautify
        workflow = self.workflow.pop(0) if isinstance(self.workflow, list) else self.workflow
        for current_step in workflow:
            while step_not_done(current_step.name, self):
                if self.step_done != current_step.name:
                    current_step.activate(self)
