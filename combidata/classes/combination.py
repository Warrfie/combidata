import copy
import traceback


def current_workflow(workflow, is_all_steps=False):
    from combidata import Process
    if isinstance(workflow[0], Process):
        for process in workflow:
            yield process
    elif is_all_steps:
        for stage in workflow:
            for process in stage:
                yield process
    else:
        for process in workflow[0]:
            yield process
        workflow.pop(0)


def step_not_done(current_step_name, combi):
    if combi.step_done != current_step_name and not isinstance(combi.step_done, Exception):
        return True
    return False


class Combination:
    """
    Represents a combination of test data and associated processes.

    Attributes:

    - test_seed (dict, optional): Formed during the ST_COMBINE process.
    - formed_data (dict, optional): Formed during the ST_FORM process.
    - step_done (str): The last successfully passed step.
    - init_lib (dict): A copy of the initial library.
    - main_case (Case): Storage for the main case instance.
    - template (dict): Holds the export template (supports JSON format).
    - tools (dict): Contains items that can be used in processes.
    - generated_data (dict): Contains all data generated during the ST_GENERATE step.
    - other_cases (dict): Stores other cases that participate in the test.
    - cache (dict): A storage for steps and processes, can store any data.
    - workflow (list or tuple): Contains a sequence of processes, can be a list of tuples or a tuple.
    """
    test_seed = None
    formed_data = None

    step_done = None  # last passed step

    def __init__(self, case, workflow, init_lib, template, tools, logger, generator_id, types_for_generation):
        self.init_lib = copy.deepcopy(init_lib)
        self.main_case = case
        self.template = template
        self.tools = tools
        self.logger = logger
        self.generator_id = generator_id

        self.generated_data = {}
        self.other_cases = {}

        self.cache = {}

        self.workflow = copy.deepcopy(workflow)

        self.types_for_generation = types_for_generation

    def run(self):
        for current_step in current_workflow(self.workflow):
            while step_not_done(current_step.name, self):
                if self.step_done != current_step.name:
                    if self.logger:
                        self.logger.start_step(self.generator_id, current_step.name)
                    try:
                        current_step.activate(self)
                    except Exception as e:
                        self.step_done = e
                        if self.logger:
                            temp_exep = f"An exception occurred: {type(e).__name__}. "
                            temp_exep += f"Error message: {str(e)}. "
                            traceback_list = traceback.extract_tb(e.__traceback__)
                            if traceback_list:
                                last_traceback = traceback_list[-1]
                                file_name = last_traceback.filename
                                line_number = last_traceback.lineno
                                temp_exep += f"Occurred at: {file_name}:{line_number}. "
                            self.logger.end_step(self.generator_id, temp_exep)
                    else:
                        if self.logger:
                            self.logger.end_step(self.generator_id)
