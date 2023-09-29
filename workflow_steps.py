from chat_handlers import openapi_wrapper, data_wrapper
from utilities import DebugValues
from typing import Optional

class WorkflowStep:
    type = None

    def __init__(self, step_id: str, step_description: str) -> None:
        self.step_id = step_id
        self.description = step_description
        return
    
    def run(self) -> str:
        """
        Abstract method to run the step. Must be implemented by subclasses.
        """
        raise NotImplementedError

class ApiDataStep(WorkflowStep):
    type = "api_access_manipulate"

    def __init__(self, step_id: str, step_description: str, openapi_doc: str, api_prompt: str, data_manipulation_prompt: Optional[str]=None) -> None:
        super().__init__(step_id, step_description)
        self.openapi_doc = openapi_doc
        self.api_prompt = api_prompt
        self.data_prompt = data_manipulation_prompt
        return
    
    def run(self, context: list[str]):
        api_result = openapi_wrapper(
        '\n'.join((context + [self.openapi_doc])),
        self.api_prompt)

        # Runs and returns data manipulation on api_result
        # only if data manipulation prompt is provided,
        # otherwise returns api_result
        if(self.data_prompt is not None):
            data_result = data_wrapper(
                '\n'.join(context + [api_result]),
                self.data_prompt)
            return data_result
        else:
            return api_result

class AskStep(WorkflowStep):
    type = "ask"

    def __init__(self, step_id: str, step_description:str, question: str, answer_key: str) -> None:
        super().__init__(step_id, step_description)
        self.question = question
        self.answer_key = answer_key
    
    def run(self):
        user_response = input(self.question)
        return f"{{ {self.answer_key} : '{user_response}' }}"
    
class Workflow:
    context = []

    def __init__(self, workflow_steps: list[WorkflowStep]) -> None:
        self.steps = workflow_steps
        return

    def run(self):
        for step in self.steps:
            if(DebugValues.verbose_logging):
                print(f"\nStep: {step.step_id}")
                print(f"Description: {step.description}")
            match (step.type):
                case ApiDataStep.type:
                    output = step.run(context=self.context)
                case AskStep.type:
                    output = step.run()
                case _:
                    # Handle undefined step types
                    #TODO Create a proper error
                    raise ValueError
            self.context.append(output)
        return