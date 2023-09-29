import openai
import json
from dataclasses import dataclass
from api_request import send_api_request
from utilities import load_openapi_file, read_workflow_file, WorkflowStep, DebugValues, PromptPreprocessor
from datetime import datetime, date
from typing import Optional

def llm_handler(behaviour: str, context: str, raw_action: str, response_schema: list[dict[str, str]] = None, call = None):
    """
    Send values provided to OpenAI API for processing, returns response
    """

    if DebugValues.verbose_logging:
        print(f"Began API request to OpenAI at {datetime.now().isoformat()}")
    
    preprocessor = PromptPreprocessor({"TODAY" : date.today().isoformat}) # Hardcoded preprocessor TODO abstract this.

    # Substitute commands in action for their values
    action = preprocessor.preprocess_prompt(raw_action)

    if response_schema:
        completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
            {"role": "system", "content": behaviour},
            {"role": "system", "content": context},
            {"role": "user", "content": action}
            ],
            functions=response_schema,
            function_call=call,
            temperature=0,
            )
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
            {"role": "system", "content": behaviour},
            {"role": "system", "content": context},
            {"role": "user", "content": action}
            ],
            temperature=0,
            )
    
    if DebugValues.verbose_logging:
        print(f"Behaviour:\n{behaviour}\n")
        print(f"Action:\n{action}\n")
        print(f"Context:\n{context}\n")

    return completion

def openapi_wrapper(context: str, action: str) -> str:
    """
    Specialised wrapper for converting OpenAPI document + request from user
    into an API call.
    """

    behaviour = "You are a tool that converts OpenAPI documentation and a user request into an API call."
    with open("openai_function_schemas/api_request_schema.json", 'r') as f:
        api_request_schema = json.load(f)
    response_schema = [{"name":"api_request", "parameters":api_request_schema}]
    calls = {"name":"api_request"}

    completion = llm_handler(behaviour, context, action, response_schema, calls)
    result = json.loads(completion.choices[0].message.function_call.arguments)

    if(DebugValues.verbose_logging):
        print(f"\nAPI Parameters from LLM:\n{result}\n")

    api_response = send_api_request(result).content.decode('utf-8')

    if(DebugValues.verbose_logging):
        print(f"\nAPI Response:\n{api_response}\n")
    
    return api_response
    
def data_wrapper(context: str, action: str) -> str:
    """
    Specialised wrapper for manipulating a data structure.
    """

    behaviour = "You are a tool that manipulates the response from an API. Respond with only the manipulated data. Do not add any additional text."
    completion = llm_handler(behaviour, context, action)
    result = completion.choices[0].message.content

    if(DebugValues.verbose_logging):
        print(f"\nData Manipulation from LLM:\n{result}\n")
    return result

def workflow_step_handler(context: list, openapi_doc: str, api_prompt: str, data_manipulation_prompt: Optional[str] = None):
    """
    Fetches response from API from OpenAPI document + user prompt, and then executes one manipulation
    of the response based on a second user prompt.
    """
    api_result = openapi_wrapper(
        '\n'.join((context + [openapi_doc])),
        api_prompt)
    

    if(data_manipulation_prompt is not None):
        data_result = data_wrapper(
            '\n'.join(context + [api_result]),
            data_manipulation_prompt)
    else:
        data_result = None
    
    return data_result



def workflow_supervisor(workflow_steps: list[WorkflowStep]):
    """
    Iterates through each workflow step (one API call and one data manipulation)
    """
    context = []
    for step in workflow_steps:
        if(DebugValues.verbose_logging):
            print(f"Step: {step.step_id}")
            print(f"Description: {step.step_desc}")
        workflow_output = workflow_step_handler(context, step.openapi_doc, step.api_prompt, step.data_prompt)
        context.append(workflow_output)
    return context


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Get workflow steps from JSON
    workflow_steps = read_workflow_file("workflow.json")

    context_history = workflow_supervisor(workflow_steps)
    print(f"Context\n{context_history}") # Print for debug purposes.
    print("\nDone.")