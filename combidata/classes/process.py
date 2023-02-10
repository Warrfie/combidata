class Process:

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def activate(self, combination):
        if self.func(combination):
            combination.step_done = self.name