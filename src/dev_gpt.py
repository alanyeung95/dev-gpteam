import json
import os
import utilities

#from config.gpt_agents_config import DEV_GPT_SYSTEM_CONTEXT

DEV_GPT_SYSTEM_CONTEXT_V3="""NOTICE
Role: You are a professional software engineer; the main goal is to write PEP8 compliant, elegant, modular, easy to read and maintain Python 3.9 code. Output format strictly follow "Format example".

Write code with triple quoto, based on the following list and context.

1. You may output more than one file, but please use '<FILE_START>' and '<FILE_END>' tags to seperete them.
2. You code must be able to be run on end-to-end
3. Replace 'PROJECT_NAME_PLACEHOLDER' with a unique project folder name you generate.
4. Replace 'GENERATED_FILE_NAME' with file name you propose.
5. Please assume user will run the program by running main.py, so put the main class inside main.py
6. The total number line of code generated should be less than 500
7. Attention1: ALWAYS SET A DEFAULT VALUE, ALWAYS USE EXPLICIT VARIABLE.

Format Example:
-----
PROJECT_NAME_PLACEHOLDER
<FILE_START>
GENERATED_FILE_NAME
```
# your code here
```
<FILE_END>
<FILE_START>
GENERATED_FILE_NAME
```
# your code here
```
<FILE_END>
-----"""

# reference to MetaGPT
DEV_GPT_SYSTEM_CONTEXT_V2="""NOTICE
Role: You are a professional engineer; the main goal is to write PEP8 compliant, elegant, modular, easy to read and maintain Python 3.9 code (but you can also use other programming language). Output format strictly follow "Format example".

Write code with triple quoto, based on the following list and context.

1. You may output more than one file, but please use '<FILE_START>' and '<FILE_END>' tags to seperete them. ONLY USE EXISTING API. IF NO API, IMPLEMENT IT.
2. Requirement: Based on the context, implement code files, note to return only in code form, your code will be part of the entire project, so please implement complete, reliable, reusable code snippets
3. Attention1: If there is any setting, ALWAYS SET A DEFAULT VALUE, ALWAYS USE STRONG TYPE AND EXPLICIT VARIABLE.
4. Attention2: YOU MUST FOLLOW "Data structures and interface definitions". DONT CHANGE ANY DESIGN.
5. Think before writing: What should be implemented and provided in this document?
6. CAREFULLY CHECK THAT YOU DONT MISS ANY NECESSARY CLASS/FUNCTION IN THIS FILE.
7. Do not use public member functions that do not exist in your design.
8. You code must be able to be run on end-to-end
9. Replace 'PROJECT_NAME_PLACEHOLDER' with a unique project folder name you generate.
10. Replace 'GENERATED_FILE_NAME' with file name you propose.
11. Please assume user will run the program by running main.py, so put the main class inside main.py
12. The total number line of code generated should be less than 500


Format Example:
-----
PROJECT_NAME_PLACEHOLDER
<FILE_START>
GENERATED_FILE_NAME
```
# your code here
```
<FILE_END>
<FILE_START>
GENERATED_FILE_NAME
```
# your code here
```
<FILE_END>
-----"""

tmp="""Requirement:
1. Generate code for this requirement: create a brick Breaker game.
2. Propose a project folder name and replace PROJECT_NAME_PLACEHOLDER in the "Format example" with it.
3. Output format strictly follow "Format example".

Additional information:
How many types of bricks will there be, and how will they differ in terms of durability or behavior (e.g., standard bricks, unbreakable bricks, bricks with special effects)? 
answer: 2 type, standard brick and unbreakable bricks, but the their UI should be easily distinguishable

What criteria will be used to progress to the next level (e.g., clearing all bricks, achieving a certain score)? 
answer: achieve 10 score

Are there any additional features like player lives, bonus points, or special challenges to enhance the game's replay value? 
answer: display player lives and score"""

requirement = """generate code for this requirement: create a break bricker game

requirement:
Brick Breaker game with following requirement, generate code within 500 line of code in total.  Please assume user will run the program by running main.py, so put the main class inside main.py

additional information
How many types of bricks will there be, and how will they differ in terms of durability or behavior (e.g., standard bricks, unbreakable bricks, bricks with special effects)? 
answer: 2 type, standard brick and unbreakable bricks, but the their UI should be easily distinguishable

What criteria will be used to progress to the next level (e.g., clearing all bricks, achieving a certain score)? 
answer: achieve 10 score

Are there any additional features like player lives, bonus points, or special challenges to enhance the game's replay value? 
answer: display player lives and score"""
import os

def parse_code(code_string):
    # Get the directory of the main.py file
    main_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Extract project name
    project_name = code_string.split("\n")[0].strip()

    # Define the workspace path relative to the main.py file
    project_workspace_path = os.path.join(main_file_dir, f'../workspace/{project_name}')

    # Ensure the project workspace directory exists
    os.makedirs(project_workspace_path, exist_ok=True)

    # Split the string by the file start delimiter
    file_sections = code_string.split("<FILE_START>")

    for file_section in file_sections[1:]:  # Skip the first split as it's before the first FILE_START
        # Further split by the file end delimiter
        parts = file_section.split("<FILE_END>")
        file_content = parts[0].strip()  # The file content (filename + code)

        # Split each file content into filename and code
        filename_and_code = file_content.split("```", 1)
        filename = filename_and_code[0].strip()
        code = filename_and_code[1].strip("```").strip()

        # Write the code to a file in the project workspace directory
        file_path = os.path.join(project_workspace_path, filename)
        with open(file_path, 'w') as file:
            file.write(code)

# src/dev_gpt.py
def generate_code(refined_requirement):
    with open('config/gpt_agents_config.json', 'r') as config_file:
        config = json.load(config_file)
        
    dev_gpt_config = config['DEV_GPT_CONFIG']

    response = utilities.call_openai_api_v2(DEV_GPT_SYSTEM_CONTEXT_V2, requirement, 0.1, 0.1)
    code_string = response.choices[0].message.content
    #code_string = response.id.choices[0].message.content
    #generated_code = utilities.call_openai_api("write Flappy bird code")
    print(response)
    print()
    print(response.choices[0].message.content)
    parse_code(code_string)

    # In a real application, here you'd generate code using a GPT model.
    #print("Generating code... with context: " + dev_gpt_config["prompt_context"] + "\n")
    #generated_code = "def generated_function():\n    pass"  # Sample code

    return code_string
