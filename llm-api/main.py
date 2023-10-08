import os
from dotenv import load_dotenv
import openai
from file_handling import read_workflow_file

if __name__ == "__main__":
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Get workflow steps from JSON
    workflow = read_workflow_file("../workflow_samples/workflow_cli.json")

    workflow.run()

    # context_history = workflow_supervisor(workflow_steps)
    # print(f"Context\n{context_history}") # Print for debug purposes.
    print("\nDone.")