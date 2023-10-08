import json
from workflow_steps import ApiDataStep, CLIAskStep, Workflow

def load_openapi_file(filename: str) -> str:
    with open(filename, 'r') as f:
        return f.read()
    
def read_workflow_file(file_path):
    """
    Construct a workflow from JSON file containing a series
    of workflow steps.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    workflow_steps = []
    for step_data in data["workflow_steps"]:
        match (step_data["step_type"]):
            case ApiDataStep.type:
                new_step = ApiDataStep(   
                    step_data["step_id"],
                    step_data["step_desc"],
                    load_openapi_file(step_data["openapi_file_location"]),
                    step_data["instruction"],
                    step_data["manipulation"]
                    )
            case CLIAskStep.type:
                new_step = CLIAskStep(
                    step_data["step_id"],
                    step_data["step_desc"],
                    step_data["question"],
                    step_data["answer_key"],
                )

        workflow_steps.append(new_step)

    return Workflow(workflow_steps)

if __name__ == "__main__":
    read_workflow_file("workflow.json")