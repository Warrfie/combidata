## Process Class Documentation

### Overview

The `Process` class represents a test step or process within the Combidata framework. It is designed to execute a specific function (referred to as `given_func`) as part of the test step. This function will continue to run until it returns `True`, indicating the completion of the process.

### Attributes

**func (function)**: 

  - Description: A function that is executed as part of the test step.
  - Requirement: This function must return `True` to indicate the completion of the process. It must also accept an argument of type `Combination`.
  - Example: 

```python
def sample_func(combination):
    # Your logic here
    return True
```

**name (str)**:

  - Description: A unique identifier for the process.
  - Requirement: The `name` must be unique across all instances to avoid conflicts.
  - Example:
  

```python
process_name = "sample_process"
```

### Usage

To define a test step, instantiate the `Process` class by providing the necessary attributes:

```python
from combidata import Process

def sample_func(combination):
    # Your logic here
    return True

process_instance = Process(name="sample_process", given_func=sample_func)
```

### Notes

- Ensure that the `name` attribute is unique to avoid any potential conflicts during execution.
- The `given_func` is essential and must always return a boolean value (`True` or `False`). It should return `True` to indicate the successful completion of the process.
- The `given_func` must accept an argument of type `Combination`. This allows you to access and manipulate the combination data within the function.