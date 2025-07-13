import os
from agent import Agent
from config import OPENROUTER_API_KEY, AGENT1_MODEL, AGENT2_MODEL

os.environ["OPENROUTER_API_KEY"] = OPENROUTER_API_KEY

def main():
    print("Initializing agents...")
    agent1 = Agent(name="Agent1", model=AGENT1_MODEL)
    agent2 = Agent(name="Agent2", model=AGENT2_MODEL)

    # Read instructions from instructions.txt
    instructions_file_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    try:
        with open(instructions_file_path, "r") as f:
            initial_instruction = f.read().strip()
    except FileNotFoundError:
        initial_instruction = "No instructions found. Agents will start a general conversation."

    print(f"\nInitial Instruction for Agents:\n{initial_instruction}\n")

    # Agent1 starts the conversation with the instruction
    agent1.add_message("user", initial_instruction)
    print(f"\n{agent1.name} is thinking...")
    agent1_response = agent1.generate_response()
    print(f"\n{agent1.name}: {agent1_response}")
    agent1.send_message(agent2, agent1_response)

    # Conversation loop
    for i in range(3):  # Limiting to 3 turns for demonstration
        print(f"\n{agent2.name} is thinking...")
        agent2_response = agent2.generate_response()
        print(f"\n{agent2.name}: {agent2_response}")
        agent2.send_message(agent1, agent2_response)

        if i < 2: # Don't let agent1 respond on the last turn
            print(f"\n{agent1.name} is thinking...")
            agent1_response = agent1.generate_response()
            print(f"\n{agent1.name}: {agent1_response}")
            agent1.send_message(agent2, agent1_response)

    print("\nInteraction complete.")

if __name__ == "__main__":
    main()