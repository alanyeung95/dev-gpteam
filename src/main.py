import pm_gpt
import dev_gpt
import qa_gpt

def main():
    print("Welcome to Dev GPTeam!")
    initial_requirement = input("Please enter your initial software requirement: ")
    
    refined_requirement = pm_gpt.refine_requirements(initial_requirement)
    generated_code = dev_gpt.generate_code(refined_requirement)
    qa_gpt.validate_code(generated_code)

    print("Code generation completed!!!")

if __name__ == "__main__":
    main()
