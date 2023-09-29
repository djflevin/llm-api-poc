import json, yaml
from dataclasses import dataclass
from datetime import date
from typing import Callable


class DebugValues:
    verbose_logging = True


def load_openapi_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()

@dataclass
class WorkflowStep:
    step_id: str
    step_type: str
    step_desc: str
    openapi_doc: str
    api_prompt: str
    data_prompt: str

def read_workflow_file(file_path):
    """
    Constructs a workflow from JSON file containing a series
    of workflow steps.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    workflow_steps = []
    for step_data in data["workflow_steps"]:
        new_step = WorkflowStep(
            step_data["step_id"],
            step_data["step_type"],
            step_data["step_desc"],
            load_openapi_file(step_data["openapi_file_location"]),
            step_data["instruction"],
            step_data["manipulation"]
            )
        workflow_steps.append(new_step)

    return workflow_steps

class PromptPreprocessor:
    def __init__(self, substitutions: dict[str: Callable]) -> None:
        self.substitutions = substitutions
        self.split_symbol = "##"
        return

    def preprocess_prompt(self, prompt: str) -> str:
        indexes = self.find_indexes_for_split(prompt, self.split_symbol)

        if len(indexes) % 2 != 0:  # Ensure there's an even number of split symbols
            raise ValueError("Mismatched split symbols in the prompt.")

        reconstructed_strings = []
        last_index = 0
        for i in range(0, len(indexes), 2):
            start, end = indexes[i], indexes[i+1]

            # Add the string slice before the current split symbol
            reconstructed_strings.append(prompt[last_index:start])

            # Extract the command and substitute it
            command = prompt[start + len(self.split_symbol):end]
            substitution_function = self.substitutions.get(command)
            if substitution_function and callable(substitution_function):
                substitution = substitution_function()
            else:
                substitution = command  # Default to the command if not found or not callable
            reconstructed_strings.append(substitution)

            last_index = end + len(self.split_symbol)

        # Add the remaining part of the string after the last split symbol
        reconstructed_strings.append(prompt[last_index:])

        preprocessed_string = "".join(reconstructed_strings)  # Flatten array back into string
        return preprocessed_string

    def find_indexes_for_split(self, s: str, pattern: str) -> list:
        indexes = []
        index = s.find(pattern)

        while index != -1:
            indexes.append(index)
            index = s.find(pattern, index + len(pattern))

        return indexes

if __name__ == "__main__":
    # Example usage:
    def get_hello():
        return "Hello"

    def get_world():
        return "World"

    substitutions = {
        "HELLO": get_hello,
        "WORLD": get_world
    }

    processor = PromptPreprocessor(substitutions)
    prompt = "This is a test ##HELLO## and another test ##WORLD##."
    print(processor.preprocess_prompt(prompt))  # Expected: "This is a test Hello and another test World."
