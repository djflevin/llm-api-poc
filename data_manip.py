import openai
import json

def get_data_manipulation_from_llm(data, user_prompt):
  completion = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=[
      {"role": "system", "content": "You are a tool that manipulates the response from an API."},
      {"role": "system", "content": "Respond with only the manipulated data. Do not add any additional text."},
      {"role": "system", "content": data},
      {"role": "user", "content": user_prompt}
      ],
      temperature=0,
  )
  return completion

def manipulate_data(data, user_prompt):
    llm_response = get_data_manipulation_from_llm(data, user_prompt)

    # Extract the GPT reply nested inside the OpenAI API response as a dictionary
    llm_reply = json.loads(llm_response.choices[0].message.content)
    return llm_reply