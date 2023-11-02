## Combidata Case User Guide

### Introduction
In Combidata, a `Case` represents a specific test scenario or variation. It is defined using a dictionary structure with specific keys that have predefined meanings. This guide will help you understand how to define a `Case` and what each key represents.

### Defining a Case
A `Case` is defined as a dictionary. Each key-value pair in the dictionary corresponds to a specific attribute or property of the case. Here's a breakdown of the keys you can use:

#### Reserved Keys:
- **name**: A descriptive name for the case. This name should be unique across the entire test to avoid confusion.
- **gen_func**: A function responsible for generating values for the case. It will accept `value` or `options` if they are provided.
- **value**: The primary value associated with the case. If `gen_func` is provided, this will be the first argument for that function. This can be of any data type.
- **options**: A dictionary that provides additional parameters or arguments for the `gen_func`. The key in this dictionary will be the argument name for the function, and the associated value will be the argument value.
- **is_presented**: A boolean flag indicating if the case should be exported or considered in the final output.
- **requirements**: Specifies dependencies on other fields. It's a dictionary where keys are field names and values are lists of field modes that this case depends on.
- **type**: Indicates the type of test this case belongs to. It should be a string. For example, "error" might indicate this case is meant to test error scenarios.

#### Additional Fields:
Any key in the `Case` dictionary that is not one of the reserved keys mentioned above is considered an "Additional Field". These fields are user-defined and can be used to store any extra information or metadata related to the case.

For example, in the provided sample, the key "error" with its associated dictionary (`{"code": 400, "message": "Sample Error Message"}`) is an additional field. It provides extra information about the error scenario being tested.

### Accessing Additional Fields
You can access the values of additional fields just like you would access any key-value pair in a dictionary:

```python
case_value = my_case["additional_field_name"]
```

### Example:
Here's a sample `Case` definition for better understanding:

```python
relatives["cases"]["FIELD_NAME"] = {
    "MODE_CODE": {
        "value": "Sample Value",
        "name": "Descriptive Name for the Case",
        "requirements": {"ANOTHER_FIELD": ["MODE_CODE_1", "MODE_CODE_2"]},
        "type": "error",
        "error": {"code": 400, "message": "Sample Error Message"}
    },
    ...
}
```

In this example:

- "FIELD_NAME" is the name of the field being tested.

- "MODE_CODE" is a unique code representing a specific test scenario or variation for "FIELD_NAME".

- The dictionary associated with "MODE_CODE" defines the properties of that specific test scenario.

### Conclusion
Defining a `Case` in Combidata involves setting up a dictionary with specific keys that have predefined meanings. The flexibility of the structure allows you to define a wide range of test scenarios and variations, making it a powerful tool for comprehensive testing.