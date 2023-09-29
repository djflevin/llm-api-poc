import openai, os
import json
from dotenv import load_dotenv

# Config
llm="gpt-4-0613"
with open("openai_function_schemas/api_request_schema.json", 'r') as f:
    api_request_schema = json.load(f)

# Main body
def generate_api_parameters_from_llm(openapi, user_prompt):
  print(api_request_schema)
  completion = openai.ChatCompletion.create(
    model=llm,
    messages=[
      {"role": "system", "content": "You are a tool that converts OpenAPI documentation and a user request into an API call."},
      {"role": "system", "content": openapi},
      {"role": "user", "content": user_prompt}
      ],
      functions=[{"name":"api_request", "parameters":api_request_schema}],
      function_call={"name":"api_request"},
      temperature=0,
  )
  return completion

def get_api_parameters(openapi, user_prompt):
    """TODO: Add docstring"""
    gpt_response = generate_api_parameters_from_llm(openapi, user_prompt)

    # Extract the GPT reply nested inside the OpenAI API response as a dictionary
    llm_reply = json.loads(gpt_response.choices[0].message.function_call.arguments)
    return llm_reply