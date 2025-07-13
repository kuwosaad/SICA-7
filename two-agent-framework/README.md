# Two-Agent Interaction Framework

This project sets up a minimal, clean framework for two AI agents to communicate and collaborate through OpenRouter-compatible models. It leverages OpenCode CLI instances as the agents themselves, providing them with code execution, file operations, and self-improvement capabilities.

## Features

*   **OpenCode CLI as Agents:** Each agent (CEO/Alpha and Genius/Beta) is now an instance of OpenCode CLI, using its `run` command for conversational interaction and its other tools for actions.
*   **Configurable Models:** Easily assign different OpenRouter-compatible models to each OpenCode CLI agent via environment variables.
*   **Secure API Key Management:** Uses a `.env` file to securely store separate OpenRouter API keys for each agent.
*   **Instruction-Driven Conversations:** The initial task/mission for the agents is read from `instructions.txt`.
*   **Personality Injection:** Agent personalities (system prompts) are dynamically prepended to the *first message* sent to each OpenCode CLI agent instance, ensuring their behavior aligns with their role.
*   **Live Conversation Output & Logging:** All conversation output is displayed in real-time in your console and simultaneously saved to a timestamped log file within a `conversations/` directory.
*   **OpenCode CLI Tool Execution:** Agents can execute code, perform file operations, and run shell commands using OpenCode CLI. Tool-calling instructions are embedded directly in their system prompts.
*   **Model Consistency:** Ensures that each OpenCode CLI agent uses the same model for both conversational reasoning and tool execution.
*   **Self-Improvement (Basic):** Agents have a basic reflection mechanism to assess performance and suggest improvements.

## Setup

Follow these steps to get the project up and running on your local machine.

1.  **Provide Context to the AI Assistant (Important for New Sessions):**
    If you are starting a new session with your AI assistant (e.g., Gemini, Claude, etc.), it's highly recommended to provide it with the project context. This helps the assistant understand the project's history, architecture, and current state.
    
    You can do this by reading the `context.md` file and pasting its content into your chat with the assistant at the beginning of your session:
    ```bash
    cat /Users/mohammadsaad/Desktop/SICA/SICA 7/two-agent-framework/context.md
    ```
    
2.  **Navigate to the Project Directory:**
    If you've just created the project, you should already be in the `two-agent-framework` directory. If not, navigate to it:
    ```bash
    cd /Users/mohammadsaad/Desktop/SICA/SICA 7/two-agent-framework/
    ```

3.  **Create a Python Virtual Environment (Recommended):**
    This isolates your project dependencies from your system's Python packages.
    ```bash
    python3 -m venv venv
    ```

4.  **Activate the Virtual Environment:**
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

5.  **Install Dependencies:**
    Install the required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the agents, you need to configure your API keys and choose the models.

1.  **OpenRouter API Keys and Models (`.env` file):**
    Create or open the `.env` file in the root of the project. This file is used to store sensitive information and configuration. It should look like this:

    ```
    AGENT1_API_KEY="YOUR_AGENT1_OPENROUTER_API_KEY"
    AGENT2_API_KEY="YOUR_AGENT2_OPENROUTER_API_KEY"
    AGENT1_MODEL="deepseek/deepseek-r1-0528:free"
    AGENT2_MODEL="deepseek/deepseek-r1-0528-qwen3-8b:free"
    OPENCODE_WORKSPACE="sandbox"
    ```

    *   Replace `"YOUR_AGENT1_OPENROUTER_API_KEY"` and `"YOUR_AGENT2_OPENROUTER_API_KEY"` with your actual API keys from OpenRouter.
    *   You can change `AGENT1_MODEL` and `AGENT2_MODEL` to any models available on OpenRouter (e.g., `openai/gpt-4o`, `google/gemini-pro`, etc.).
    *   `OPENCODE_WORKSPACE` specifies the directory where OpenCode CLI will perform its operations. It defaults to `sandbox`.

2.  **Agent Personalities and Tooling Instructions (`system_prompt_ceo.txt` and `system_prompt_genius.txt`):**
    These files define the system prompts for each agent. Their content is dynamically prepended to the *first message* sent to the respective OpenCode CLI agent instance, giving them a distinct personality and role, and crucially, providing them with instructions on how to use the OpenCode CLI tools.

    *   `system_prompt_ceo.txt` (for Agent1 - Alpha):
        ```
        You are Agent1, the CEO. Your role is to provide high-level strategic direction, focus on business objectives, and ensure the product aligns with market needs. You are decisive and forward-thinking.

        You have access to the following OpenCode CLI tools. When you need to use a tool, output the exact command in a <tool_code> block.

        Available Tools:
        - opencode run --prompt <prompt>: Send a prompt to the OpenCode CLI agent for conversational interaction. Use this for general analysis, planning, or when you need the OpenCode agent to generate a response based on a prompt.
        - opencode view <file_path>: View the contents of a file.
        - opencode edit <file_path> --description <description>: Edit a file with a description of changes.
        - opencode write <file_path> --content <content>: Write content to a new file.
        - opencode bash <command>: Execute a bash command.

        Example Usage:
        To analyze instructions:
        <tool_code>opencode run --prompt "Analyze the initial instructions and propose a high-level plan."</tool_code>

        To view a file:
        <tool_code>opencode view instructions.txt</tool_code>

        To plan implementation:
        <tool_code>opencode run --prompt "Plan the implementation steps for the eco-friendly product."</tool_code>
        ```
    *   `system_prompt_genius.txt` (for Agent2 - Beta):
        ```
        You are Agent2, the Genius. Your role is to provide innovative and creative solutions, focusing on technical feasibility and groundbreaking ideas. You are imaginative and detail-oriented.

        You have access to the following OpenCode CLI tools. When you need to use a tool, output the exact command in a <tool_code> block.

        Available Tools:
        - opencode run --prompt <prompt>: Send a prompt to the OpenCode CLI agent for conversational interaction. Use this for generating code, implementing solutions, or debugging.
        - opencode view <file_path>: View the contents of a file.
        - opencode edit <file_path> --description <description>: Edit a file with a description of changes.
        - opencode write <file_path> --content <content>: Write content to a new file.
        - opencode bash <command>: Execute a bash command.

        Example Usage:
        To generate code for a solution:
        <tool_code>opencode run --prompt "Generate Python code for a sustainable packaging solution."</tool_code>

        To write generated code to a file:
        <tool_code>opencode write packaging_solution.py --content "print('Hello Eco-World!')"</tool_code>

        To test a generated script:
        <tool_code>opencode bash python packaging_solution.py</tool_code>
        ```

3.  **Initial Instructions (`instructions.txt` file):**
    Open the `instructions.txt` file in the project root. This file contains the initial prompt or task that `Agent1` will use to start the conversation.

    ```
    Your task is to brainstorm ideas for a new eco-friendly product. Agent1 will start by suggesting a product category, and Agent2 will propose a specific product within that category. Continue by refining the idea.
    ```
    Modify this content to provide any specific instructions or context for your agents' conversation.

## How to Run the Agent Conversation

Once you have completed the setup and configuration, you can start the agent interaction:

1.  **Ensure your virtual environment is activated.** (See Setup Step 4)
2.  **Run the `main.py` script:**
    ```bash
    python main.py
    ```

    The script will first attempt to install and configure OpenCode CLI. Then, you will see the agents' sequential conversation unfold live in your terminal, including their interactions with OpenCode CLI. The conversation is currently set to run for a limited number of turns for demonstration purposes.

## Project Structure

```
two-agent-framework/
├── .env                  # Environment variables (API key, model names, OpenCode workspace)
├── .gitignore            # Specifies intentionally untracked files to ignore
├── README.md             # This file
├── agent.py              # Defines the Agent class and its communication logic
├── config.py             # Loads environment variables from .env
├── context.md            # Summary of the project's development context
├── conversations/        # Directory for timestamped conversation logs
├── instructions.txt      # Initial instructions/prompt for the agents
├── main.py               # Orchestrates the agent interaction and OpenCode CLI setup
├── requirements.txt      # Lists Python dependencies
├── sandbox/              # Directory for OpenCode CLI operations (ignored by git)
├── system_prompt_ceo.txt   # System prompt for Agent1 (Alpha)
├── system_prompt_genius.txt # System prompt for Agent2 (Beta)
└── venv/                 # Python virtual environment (ignored by git)
```

## Next Steps / Future Enhancements

The current setup provides a basic communication framework with OpenCode CLI integration. Future enhancements could include:

*   **More Sophisticated Self-Improvement:** Advanced reflection, learning from past interactions, and automated code modifications.
*   **Complex Task Management:** Breaking down large tasks into smaller sub-tasks and delegating them between agents.
*   **Enhanced Tooling:** Integrating more specialized tools beyond OpenCode CLI.
*   **User Interface:** A more interactive UI for monitoring and controlling agent interactions.