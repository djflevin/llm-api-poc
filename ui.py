from file_handling import read_workflow_file
from workflow_steps import TextInputStep, ApiDataStep
import utilities
from gradio.components import textbox
import gradio as gr

workflow = read_workflow_file("workflow.json")
utilities.load_apikey_from_env()


def get_workflow_outputs(text_input) -> list[str]:
    """
    Get workflow outputs from user input.
    """       
    full_output = []
    for step in workflow.steps:
        match (step.type):
            case ApiDataStep.type:
                step_output = step.run(workflow.context)
            case TextInputStep.type:
                step_output = step.run(text_input)
            case _:
                step_output = "Error: Step type not recognized."
        workflow.context.append(step_output)
        workflow.log.append({"step_id": step.step_id, "step_description": step.description, "output": step_output})
        full_output += [step.step_id, step.description, step_output]
    return full_output


with gr.Blocks() as demo:   

  with gr.Group():
    with gr.Row():
      question = gr.Textbox(label = "Enter the name of the patient.")
    run_btn = gr.Button("Run Workflow", variant = "primary", size = "lg")
    
  with gr.Group():
    with gr.Row():
        step_1_id = gr.Textbox(label = "Step ID")
        step_1_desc = gr.Textbox(label = "Step Description")
        step_1_output = gr.Textbox(label = "Output")
    with gr.Row():
        step_2_id = gr.Textbox(label = "Step ID")
        step_2_desc = gr.Textbox(label = "Step Description")
        step_2_output = gr.Textbox(label = "Output")
    with gr.Row():
        step_3_id = gr.Textbox(label = "Step ID")
        step_3_desc = gr.Textbox(label = "Step Description")
        step_3_output = gr.Textbox(label = "Output")
    with gr.Row():
        step_4_id = gr.Textbox(label = "Step ID")
        step_4_desc = gr.Textbox(label = "Step Description")
        step_4_output = gr.Textbox(label = "Output")

    run_btn.click(fn = get_workflow_outputs, inputs = [question], outputs = [step_1_id, step_1_desc, step_1_output, step_2_id, step_2_desc, step_2_output, step_3_id, step_3_desc, step_3_output, step_4_id, step_4_desc, step_4_output])
    
    
if __name__ == "__main__":
    demo.launch()
