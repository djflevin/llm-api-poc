from api_llm import get_api_parameters
from api_request import send_api_request
from data_manip import manipulate_data
import openai, os, json
from dotenv import load_dotenv

def klarna_test():
    with open("openapi_samples/klarna_openapi.json", 'r') as f:
        klarna = f.read()

    request = get_api_parameters(klarna, "Find an iPhone in the US")

    response = send_api_request(request)
    print(response)

    data = response.content.decode('utf-8')
    print(data)

    print("\n\n----------------------------\n\n")

    manipd_data = manipulate_data(data, "Get the information for the first item.")
    print(manipd_data)

    return

def slot_booking_test_1():
    response = """
    {
        "slots": [
            {
                "slotID": "SLOT001",
                "dateTime": "2023-09-10T10:00:00Z",
                "durationMinutes": 60
            },
            {
                "slotID": "SLOT002",
                "dateTime": "2023-09-11T15:00:00Z",
                "durationMinutes": 60
            },
            {
                "slotID": "SLOT003",
                "dateTime": "2023-09-12T17:00:00Z",
                "durationMinutes": 60
            },
            {
                "slotID": "SLOT004",
                "dateTime": "2023-09-14T11:00:00Z",
                "durationMinutes": 60
            },
            {
                "slotID": "SLOT005",
                "dateTime": "2023-09-15T09:00:00Z",
                "durationMinutes": 60
            }
        ]
    }
    """

    print(f"\n\n{response}\n\n")

    prompt = "Select earliest slot."
    print(f'Prompt: {prompt}')

    print(f"\n\n{manipulate_data(response, prompt)}\n\n")

    return

def slot_booking_test_2():
    with open ("openapi_samples/appointments_openapi.yaml", 'r') as f:
        openapi = f.read()

    p = get_api_parameters(openapi, "Get available slots for 2023-09-10 at 10:00:00 for 60 minutes.")
    response = send_api_request(p).content.decode('utf-8')

    print(f"\n\n{response}\n\n")

    return

def slot_booking_test_complete():
    with open ("openapi_samples/appointments_openapi.yaml", 'r') as f:
        openapi = f.read()

    prompt1 = "Get available slots for next week staring from Monday. Today's date is 2023-09-05."
    print(f'Prompt: {prompt1}')

    p = get_api_parameters(openapi, prompt1)
    response = send_api_request(p).content.decode('utf-8')

    
    print(f"\n\n{response}\n\n")

    prompt2 = "Select earliest slot."
    print(f'Prompt: {prompt2}')

    print(f"\n\n{manipulate_data(response, prompt2)}\n\n")

    return

def get_patient_test():
    with open ("openapi_samples/patients_openapi.yaml", 'r') as f:
        openapi = f.read()

    prompt = "Get the patient Jane Smith, a woman."
    print(f'Prompt: {prompt}')

    p = get_api_parameters(openapi, prompt)
    response = send_api_request(p).content.decode('utf-8')

    print(f"\n\n{response}\n\n")

    return

def send_email_test():
    with open("openapi_samples/email_openapi.yaml", 'r') as f:
        openapi = f.read()
    
    prompt = "Send an email to the clinicalbookings@nhs.uk to book an appointment for Jane Smith at 10:00 on 2023-09-09"
    print(f'Prompt: {prompt}')

    p = get_api_parameters(openapi, prompt)
    response = send_api_request(p).content.decode('utf-8')

    print(f"\n\n{response}\n\n")

    return

def chain_test():
    with open ("openapi_samples/appointments_openapi.yaml", 'r') as f:
        appointments_openapi = f.read()
    with open ("openapi_samples/patients_openapi.yaml", 'r') as f:
        patients_openapi = f.read()
    with open ("openapi_samples/email_openapi.yaml", 'r') as f:
        email_openapi = f.read()
    
    appointments_prompt_1 = "Get available slots for next week starting from Monday. Today's date is 2023-09-05."

    print(f'\n\nPrompt: {appointments_prompt_1}')

    appointments_p = get_api_parameters(appointments_openapi, appointments_prompt_1)
    appointments_response = send_api_request(appointments_p).content.decode('utf-8')

    print(f"\n\n{appointments_response}\n\n")

    appointments_prompt_2 = "Select earliest slot."

    print(f'\n\nPrompt: {appointments_prompt_2}')

    appointments_manipd_data = manipulate_data(appointments_response, appointments_prompt_2)

    print(f"\n\n{appointments_manipd_data}\n\n")

    patients_prompt_1 = "Find the details of the patient Jane Smith, a woman."

    print(f'\n\nPrompt: {patients_prompt_1}')

    patients_p = get_api_parameters(patients_openapi, patients_prompt_1)
    patients_response = send_api_request(patients_p).content.decode('utf-8')

    print(f"\n\n{patients_response}\n\n")

    patients_prompt_2 = "Get the patient's name and NHS number."

    print(f'\n\nPrompt: {patients_prompt_2}')

    patients_manipd_data = manipulate_data(patients_response, patients_prompt_2)

    print(f"\n\n{patients_manipd_data}\n\n")

    email_prompt_1a = "Send an email to clinicalappointments@nhs.uk to book an appointment for the following details"
    email_prompt_1 = f"{email_prompt_1a}\n\n{appointments_manipd_data}\n\n{patients_manipd_data}"

    print(f'\n\nPrompt: {email_prompt_1}')

    email_p = get_api_parameters(email_openapi, email_prompt_1)

    email_response = send_api_request(email_p).content.decode('utf-8')

    print(f"\n\n{email_response}\n\n")

    print("\n\nComplete.")
    return



if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    chain_test()

