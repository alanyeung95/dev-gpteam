import json
import os
import utilities
from time import sleep

from openai import OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') 
OPENAI_API_ENDPOINT = os.getenv('OPENAI_API_ENDPOINT') 
client = OpenAI()

def extract_req(text):
    start_marker = "<REQ_START>"
    end_marker = "<REQ_END>"
    start_index = text.find(start_marker)
    if start_index == -1:
        return "Start marker not found"

    # Adjust start_index to get the end of the start_marker
    start_index += len(start_marker)

    end_index = text.find(end_marker, start_index)
    if end_index == -1:
        return "End marker not found"

    # Extract the part of the string between the markers
    return text[start_index:end_index]

# src/pm_gpt.py
def refine_requirements(initial_requirement):
    with open('config/gpt_agents_config.json', 'r') as config_file:
        config = json.load(config_file)
        
    dev_gpt_config = config['PM_GPT_CONFIG']

    ## create/retrieve assistant
    # assistant = client.beta.assistants.create(
    #     name=dev_gpt_config["role"],
    #     instructions=dev_gpt_config["prompt_context"],
    #     tools=[],
    #     model= "gpt-3.5-turbo-1106" #"gpt-4-1106-preview" # gpt-4 is better, but 3.5 is accaptable 
    # )
    assistant = client.beta.assistants.retrieve("asst_yWhWMtivHAQNUwH4f8pIY8Hu") # this is a established 3.5 assistant

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=initial_requirement
    )
    print("user: " + initial_requirement)


    # iteratively clarify requirements until client satisfies
    while True:
        # run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        # print(run)

        # check run status. wait until finish
        finish = False
        while not finish: 
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            finish = run.status == "completed"
            sleep(3) # not a good practice but useful

        # get message list
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # for msg in reversed(messages.data):
        #     print(msg.role + ": " + msg.content[0].text.value)

        # print latest message
        response =  messages.data[0].content[0].text.value
        print(messages.data[0].role + ": " + response)

        # if the assistant repsonse contains the final requirement, break clarifying loop
        if "<REQ_START>" in response:
            refined_requirement = extract_req(response)
            break
        
        # else, continue iteration
        user_input = input("user: ")
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

    return refined_requirement


if __name__ == "__main__":
    refined_requirement = refine_requirements("I want to build a flappy bird game")
    print("Requirements:")
    print(refined_requirement)