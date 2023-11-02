## Combination Class Documentation

---

### Overview:

The `Combination` class represents a combination of test data and associated processes. It plays a crucial role in the test generation process and is utilized within various process classes. It provides a structured way to manage and manipulate test data during the execution of test processes.

---

### Key Features:

- **Integration with Process Classes**: The `Combination` class is passed as an argument to process classes, making it an essential component for test generation and execution.

- **Cache Usage**: Within the processes, the `cache` attribute of the `Combination` class can be utilized. This dictionary attribute allows for the addition, modification, and retrieval of key-value pairs, facilitating dynamic data storage and manipulation during test execution.

- **Emergency Stop**: In unforeseen situations where a process needs to be halted immediately, the `step_done` attribute can be set to "STOP" (in uppercase). This signals an immediate termination of the current process.

- **Access in Generation Function**: The `Combination` class can be accessed within the Generation function. By using the `Options` key and setting its value to the reserved word "combination", the class instance can be retrieved and manipulated.

---

### Usage:

When defining a process, ensure that the `Combination` class is passed as an argument. This allows for seamless integration and data flow between the test generation logic and the processes. The `cache` attribute can be used for temporary data storage, and in case of any unexpected issues, the process can be stopped by setting `step_done` to "STOP".

---

### Attributes:

- **test_seed**: A dictionary that is formed during the ST CombineProcess. It's optional and might not be used if the ST CombineProcess is not invoked.
  
- **formed_data**: A dictionary that is formed during the ST FormProcess. It's optional and might not be used if the ST FormProcess is not invoked.

- **step_done**: A string indicating the last successful step.

- **init_lib**: A dictionary that is a copy of the initial library.

- **main_case**: An instance of the main case.

- **template**: A dictionary that holds the export template.

- **tools**: A dictionary containing intangible user tools.

- **generated_data**: A dictionary holding all data generated during the ST Generate step.

- **other_cases**: A dictionary storing other cases that take part in the test.

- **cache**: A dictionary that serves as a store for your steps and processes. It can be used to store any data that might be needed during the execution of processes.

- **workflow**: Either a list or tuple containing processes.

---

This documentation provides a comprehensive overview of the `Combination` class, its attributes, and how it can be used within process functions.
