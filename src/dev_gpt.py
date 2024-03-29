import json
import os
import utilities

from openai import OpenAI

from gpt_agent_config.dev_config import DEV_GPT_SYSTEM_CONTEXT
from gpt_agent_config.dev_config import DEV_GPT_ADDITIONAL_REQUIREMENT

DEV_GPT_TEMPERATURE_N_TOPP = float(os.getenv('DEV_GPT_TEMPERATURE_N_TOPP'))

client = OpenAI()

# src/dev_gpt.py
def generate_code(refined_requirement):
    # attention: the '#' in the beginning may make GPT ignore the rest of the content 
    prompt = refined_requirement.strip().strip("#") + "\n" + DEV_GPT_ADDITIONAL_REQUIREMENT

    response = utilities.call_openai_api_DEV(DEV_GPT_SYSTEM_CONTEXT, prompt, DEV_GPT_TEMPERATURE_N_TOPP, DEV_GPT_TEMPERATURE_N_TOPP, model="gpt-4-1106-preview")
    code_string = response.choices[0].message.content

    #print(response.usage)

    return code_string