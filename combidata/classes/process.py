class Process:
    """
    Holds test step (process)

    Given func will run until True returns
    Name must be uniq
    """

    def __init__(self, name: str, func):
        self.name = name
        self.func = func

    def activate(self, combination):
        if self.func(combination):
            combination.step_done = self.name