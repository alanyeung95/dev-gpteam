import pm_gpt
import dev_gpt
import qa_gpt

def main():
    print("Welcome to Dev GPTeam!")
    initial_requirement = input("Please enter your initial software requirement: ")
    
    refined_requirement = pm_gpt.refine_requirements(initial_requirement)

    tmp_requirement="""
    Generate code for this requirement: create a brick Breaker game.

    Requirement:
    Brick Layout: The game must initialize with bricks arranged in a specific pattern (rows and columns) on the screen.
    Paddle Control: Players should be able to control the horizontal movement of a paddle using keyboard, mouse, or touch inputs.
    Ball Mechanics: A ball must bounce off walls, the paddle, and bricks, following proper physics for reflection angles.
    Brick Collision: When the ball collides with a brick, the brick should disappear, and the player's score should increase.
    Lives: The game should start with a predetermined number of lives. A life is lost when the ball passes the paddle and hits the bottom.
    Scoring System: The game must have a scoring system where points are awarded for breaking bricks.
    Game Over Condition: The game should end when either all bricks are broken (win) or the player loses all lives (lose).
    User Interface: The game should display the current score, number of lives, and any relevant instructions or buttons (e.g., start, restart).
    """

    generated_code = dev_gpt.generate_code(tmp_requirement)
    #qa_gpt.validate_code(generated_code)

    print("Code generation completed!!!")

if __name__ == "__main__":
    main()
