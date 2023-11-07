import json

import utilities

# src/dev_gpt.py
def generate_code(refined_requirement):
    with open('config/gpt_agents_config.json', 'r') as config_file:
        config = json.load(config_file)
        
    dev_gpt_config = config['DEV_GPT_CONFIG']

    generated_code = utilities.call_openai_api("user", "write code for two sum")
    #generated_code = utilities.call_openai_api("write Flappy bird code")
    print(generated_code)

    # In a real application, here you'd generate code using a GPT model.
    #print("Generating code... with context: " + dev_gpt_config["prompt_context"] + "\n")
    #generated_code = "def generated_function():\n    pass"  # Sample code

    return generated_code
