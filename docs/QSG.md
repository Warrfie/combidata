---
hide:
  - navigation
---

## Quick Start Guide

Welcome to Combidata, a case-oriented library designed for compositional testing of combinatorics in IT product functionalities. This guide will walk you through the basic structure and usage of Combidata to help you get started quickly.

### Overview

Combidata allows you to define test cases and workflows, and then generate test data based on these definitions. It provides a flexible and powerful way to handle combinatorial testing, ensuring that all possible combinations of inputs are tested.

### Structure of Input Library

The main structure of the input library is as follows:

```python
library = {
    "cases": {},
    "workflow": (ST_COMBINE, ST_GENERATE, ST_FORM),
    "tools": {},
    "template": {}
}
```

- **cases**: Contains a library instance with all your defined test cases.
- **workflow**: Stores a tuple or list of processes to be executed during the test generation.
- **tools**: A dictionary of utilities and functions that can be used within the processes.
- **template**: Defines the format for exporting the test results.

### Defining Cases

Cases are the heart of Combidata. They define the different test scenarios you want to cover. Each case is associated with a field, and each field can have multiple cases. Here's a brief overview of the case structure:

```python
library["cases"]["FIELD_NAME"] = {
    "CASE_CODE": {
        "name": "Description of the case",
        "gen_func": function_for_generation,
        "value": "Value or pattern for the case",
        "options": {"key": "value"},
        "is_presented": True/False,
        "requirements": {"AnotherField": "CaseCode"},
        "type": "Type of the case"
    }
}
```

- **name**: A unique description of the case.
- **gen_func**: A function that generates the test data for the case.
- **value**: The value or pattern that the test data should match.
- **options**: Additional options for the generation function.
- **is_presented**: Determines if the case should be included in the exported results.
- **requirements**: Specifies dependencies on other fields.
- **type**: The type of the case, used for filtering during test generation.

### Workflow

The workflow defines the sequence of processes that Combidata will execute during test generation. You can define a single workflow or multiple workflows based on your testing needs.

```python
"workflow": (ST_COMBINE, ST_GENERATE, ST_FORM)
```

Each process in the workflow is an instance of the `Process` class, which takes a name and a function. The function should return `True` when it's done, or you can stop the workflow prematurely using `combination.step_done = "STOP"`.

### Tools

The tools section is a warehouse for utilities, functions, or any other resources you might need during test generation. You can access these tools within your processes using `combination.tools["TOOL_NAME"]`.

### Template

The template defines the format of the exported test results. It's a simple dictionary where each key is a field name, and the value is the case code. Combidata will replace these placeholders with the generated test data.

### Running Tests

Once you've defined your library, you can create an instance of the `DataGenerator` class and call its `run()` method to generate test data. Here's a simple example:

```python
generator = DataGenerator(library)
generator.run()
```

You can then use the generated combinations in your tests. For instance, using pytest:

```python
@pytest.mark.parametrize("combination_name", generator.combinations.keys())
def test(combination_name):
    combination = generator.combinations[combination_name]
    combination.run()
    # Your test assertions here
```

### Conclusion

Combidata provides a powerful and flexible way to handle combinatorial testing in IT products. By defining cases, workflows, and templates, you can ensure comprehensive test coverage for your product's functionalities. Whether you're new to compositional testing or an experienced tester, Combidata offers the tools and flexibility you need to achieve your testing goals.