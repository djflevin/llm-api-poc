from chat_handlers import llm_handler
import json
from time import sleep

results_filename = "results.json"

prompts = [
    "Search for an iPhone 15 in the U.S. marketplace",
    "Locate iPhone 15 on United States store",
    "Show me where to find iPhone 15 in the U.S. store",
    "Retrieve iPhone 15 availability in US-based shops",
    "Query U.S. store for iPhone 15",
    "Discover iPhone 15 in United States retail outlets",
    "Explore options for iPhone 15 in U.S. stores",
    "Find me iPhone 15 listings in U.S. stores",
    "Identify where iPhone 15 is sold in the United States",
    "Scan U.S. shops for the iPhone 15",
    "Uncover iPhone 15 offers in U.S. retail",
    "Reveal the iPhone 15 in American stores",
    "Search U.S. outlets for iPhone 15 availability",
    "Investigate iPhone 15 in U.S. market",
    "Pinpoint iPhone 15 in United States online store",
    "Check U.S. vendors for iPhone 15",
    "Examine availability of iPhone 15 in the United States",
    "Seek out iPhone 15 in U.S. commercial establishments",
    "Find iPhone 15 from U.S. sellers",
    "Retrieve listings of iPhone 15 in U.S. commerce",
    "Inspect U.S. inventory for iPhone 15",
    "Survey U.S. marketplaces for iPhone 15",
    "Ascertain iPhone 15's presence in U.S. shops",
    "View iPhone 15 options in the United States",
    "Highlight iPhone 15 in U.S. retail locations",
    "Inquire about iPhone 15 in United States stores",
    "Procure information on iPhone 15 in U.S. retail",
    "Detect iPhone 15 in the United States market",
    "Analyze U.S. shop listings for iPhone 15",
    "Browse for iPhone 15 in American outlets",
    "Source iPhone 15 from U.S. stores",
    "Evaluate U.S. stock levels for iPhone 15",
    "Search for iPhone 15 within United States commerce",
    "Determine iPhone 15 availability in U.S. outlets",
    "Collect data on iPhone 15 in American stores",
    "Register iPhone 15 options in U.S. market",
    "Monitor U.S. stores for iPhone 15 inventory",
    "Look up iPhone 15 in United States shopping platforms",
    "Trace iPhone 15 offers in American retail",
    "Assess U.S. availability of iPhone 15",
    "Focus on finding iPhone 15 in U.S. venues",
    "Confirm the sale of iPhone 15 in U.S. stores",
    "Delve into U.S. platforms for iPhone 15 listings",
    "Survey U.S. e-commerce for iPhone 15",
    "Unearth iPhone 15 options in U.S. retail",
    "Gather intelligence on iPhone 15 in United States shops",
    "Expose available iPhone 15 in U.S. market",
    "Take stock of iPhone 15 in United States retailers",
    "Discern the availability of iPhone 15 in U.S. commerce",
    "Appraise U.S. sellers for iPhone 15 inventory",
    "Scrutinize iPhone 15's presence in American outlets",
    "Catalog iPhone 15 found in U.S. stores",
    "Investigate the U.S. sales landscape for iPhone 15",
    "Elucidate options for acquiring iPhone 15 in U.S.",
    "Audit U.S. stock for iPhone 15 availability",
    "Validate iPhone 15 listings in U.S. retail spaces",
    "Reconnoiter U.S. vendors for iPhone 15",
    "Peruse U.S. marketplace for iPhone 15",
    "Tabulate iPhone 15 offerings in United States market",
    "Study U.S. listings for availability of iPhone 15",
    "Scrutinize U.S. retail options for iPhone 15",
    "Investigate iPhone 15 status in U.S. shops",
    "Probe U.S. market for iPhone 15",
    "Enumerate U.S. sellers offering iPhone 15",
    "Distinguish U.S. stores with iPhone 15 in stock",
    "Perceive iPhone 15 availability in U.S. retail",
    "Interrogate U.S. marketplace for iPhone 15",
    "Sift through U.S. vendors for iPhone 15",
    "Contrast iPhone 15 options in U.S. stores",
    "Map out iPhone 15 availability in U.S. outlets",
    "Query for iPhone 15 within U.S. shopping platforms",
    "Extrapolate iPhone 15 options in American market",
    "Review iPhone 15 presence in United States stores",
    "Annotate iPhone 15 listings in U.S. retail",
    "Compile U.S. shops selling iPhone 15",
    "Qualify iPhone 15 offers in United States market",
    "Summarize iPhone 15 availability in U.S. commerce",
    "Cross-reference iPhone 15 in American outlets",
    "Gauge U.S. inventory levels for iPhone 15",
    "Inspect U.S. storefronts for iPhone 15",
    "Examine U.S. retail databases for iPhone 15",
    "Corroborate iPhone 15 listings in American stores",
    "Check U.S. e-commerce platforms for iPhone 15",
    "Survey U.S. vendors for iPhone 15 stock",
    "Decipher iPhone 15 availability in United States commerce",
    "Measure U.S. retail supply of iPhone 15",
    "Track down iPhone 15 in U.S. stores",
    "Cull iPhone 15 options from U.S. market",
    "Assay iPhone 15 availability in United States retail",
    "Probe for iPhone 15 in American commerce",
    "Collate U.S. listings for iPhone 15",
    "Investigate U.S. retail channels for iPhone 15",
    "Evaluate U.S. e-commerce for iPhone 15",
    "Search American retail databases for iPhone 15",
    "Sum up iPhone 15 options in U.S. shops",
    "Audit United States retail for iPhone 15",
    "Synchronize U.S. iPhone 15 listings",
    "Clarify iPhone 15 availability in U.S. market",
    "Filter U.S. stores for iPhone 15 options",
    "Extricate iPhone 15 listings from U.S. commerce"
]

with open("openapi_samples/klarna_openapi.json", 'r') as f:
    klarna = f.read()

def load_results():
    try:
        with open(results_filename, "r") as file:
            current_results = json.load(file)
    except:
        print("No previous state information found")
        current_results = {}
    return current_results

def write_results(results):
    with open(results_filename, "w") as file:
        json.dump(results, file)
    return


def make_request(context, action: str) -> str:
    behaviour = "You are a tool that converts OpenAPI documentation and a user request into an API call."
    with open("openai_function_schemas/api_request_schema.json", 'r') as f:
        api_request_schema = json.load(f)

    response_schema = [{"name":"api_request", "parameters":api_request_schema}]
    calls = {"name":"api_request"}

    completion = llm_handler(behaviour, context, action, response_schema, calls)
    result = json.loads(completion.choices[0].message.function_call.arguments)
    return result

if __name__ == "__main__":
    print("Run")
    import openai, os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_TESTING_KEY")

    print("Running test prompt sensitivity")
    print("This will take a while...")
    print(f"Results will be saved to {results_filename}")

    for prompt in prompts:
        current_results = load_results()

        output = make_request(klarna, prompt)
        current_results[prompt] = output

        write_results(current_results)

        print(f"\n\nPrompt: {prompt}\n\nOutput:\n{output}\n\n")

        sleep(10)