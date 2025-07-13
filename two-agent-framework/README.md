# Two-Agent Interaction Framework

This project sets up a minimal, clean framework for two AI agents to communicate and collaborate. The goal is to create a flexible environment where agents can interact, and eventually, gain the ability to integrate and build their own tools for self-improvement.

## Features

*   **Two-Agent Communication:** A basic setup for two distinct AI agents to exchange messages.
*   **Configurable Models:** Easily assign different OpenRouter-compatible models to each agent via environment variables.
*   **Secure API Key Management:** Uses a `.env` file to securely store your OpenRouter API key.
*   **Instruction-Driven Conversations:** Agents can be given an initial task or prompt via an `instructions.txt` file.
*   **Live Conversation Output:** View the agents' conversation in real-time in your console.

## Setup

Follow these steps to get the project up and running on your local machine.

1.  **Navigate to the Project Directory:**
    If you've just created the project, you should already be in the `two-agent-framework` directory. If not, navigate to it:
    ```bash
    cd /Users/mohammadsaad/Desktop/SICA/SICA 7/two-agent-framework/
    ```

2.  **Create a Python Virtual Environment (Recommended):**
    This isolates your project dependencies from your system's Python packages.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    Install the required Python libraries using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Before running the agents, you need to configure your API key and choose the models.

1.  **OpenRouter API Key and Models (`.env` file):**
    Create or open the `.env` file in the root of the project. This file is used to store sensitive information and configuration. It should look like this:

    ```
    OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"
    AGENT1_MODEL="deepseek/deepseek-r1-0528:free"
    AGENT2_MODEL="deepseek/deepseek-r1-0528-qwen3-8b:free"
    ```

    *   Replace `"YOUR_OPENROUTER_API_KEY"` with your actual API key from OpenRouter.
    *   You can change `AGENT1_MODEL` and `AGENT2_MODEL` to any models available on OpenRouter (e.g., `openai/gpt-4o`, `google/gemini-pro`, etc.).

2.  **Initial Instructions (`instructions.txt` file):**
    Open the `instructions.txt` file in the project root. This file contains the initial prompt or task that `Agent1` will use to start the conversation.

    ```
    Your task is to brainstorm ideas for a new eco-friendly product. Agent1 will start by suggesting a product category, and Agent2 will propose a specific product within that category. Continue by refining the idea.
    ```
    Modify this content to provide any specific instructions or context for your agents' conversation.

## How to Run the Agent Conversation

Once you have completed the setup and configuration, you can start the agent interaction:

1.  **Ensure your virtual environment is activated.** (See Setup Step 3)
2.  **Run the `main.py` script:**
    ```bash
    python main.py
    ```

    You will see the agents' conversation unfold live in your terminal. The script is currently set to run for 3 turns, but you can adjust this in `main.py` by changing the `range()` value in the conversation loop.

## Project Structure

```
two-agent-framework/
├── .env                  # Environment variables (API key, model names)
├── .gitignore            # Specifies intentionally untracked files to ignore
├── README.md             # This file
├── agent.py              # Defines the Agent class and its communication logic
├── config.py             # Loads environment variables from .env
├── instructions.txt      # Initial instructions/prompt for the agents
├── main.py               # Orchestrates the agent interaction
└── requirements.txt      # Lists Python dependencies
└── venv/                 # Python virtual environment (ignored by git)
```

## Next Steps / Future Enhancements

The current setup provides a basic communication framework. Future enhancements could include:

*   **Tool Integration:** Giving agents access to external tools (e.g., shell commands, file I/O, web search) to perform tasks.
*   **Self-Improvement Loop:** Agents could be tasked with identifying and integrating new tools or even modifying their own code.
*   **More Sophisticated Conversation Management:** Implementing more complex turn-taking, memory management, and goal-oriented dialogues.
