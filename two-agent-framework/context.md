# Conversation Context Summary

This document summarizes the key decisions, implementations, and current state of the "Two-Agent Interaction Framework" project. It serves as a persistent memory for future interactions and development.

## Project Goal
To build a minimal, clean framework for two AI agents to communicate and collaborate, gradually giving them access to tools and enabling self-improvement.

## Core Architecture
- **Agents:** Two agents, Alpha (CEO/Planner) and Beta (Genius/Executor), with distinct personalities defined by system prompts.
- **Communication:** Agents communicate via a shared Python `queue` for sequential, turn-based interaction.
- **Model Configuration:** Each agent uses a specific OpenRouter-compatible model and its own dedicated API key, loaded from a `.env` file.
- **Tooling:** Integrated OpenCode CLI for code execution, file operations, and shell commands. OpenCode CLI calls are made with the calling agent's specific model and API key.
- **Instructions:** Initial task/mission for the agents is read from `instructions.txt`.
- **Logging:** All conversation output is logged to a timestamped file within a `conversations/` directory, while also being displayed live in the console.
- **Workspace:** OpenCode CLI operations are performed within a `sandbox/` directory.
- **Self-Improvement:** Basic reflection and improvement capabilities are stubbed out.

## Key Decisions & Implementations
- **Separate API Keys:** Implemented `AGENT1_API_KEY` and `AGENT2_API_KEY` in `.env` and updated `config.py`, `agent.py`, and `main.py` to use them.
- **OpenCode CLI Integration:**
    - `agent.py` now contains methods (`opencode_run_prompt`, `opencode_view_file`, `opencode_write_file`, `opencode_bash_command`, etc.) that directly invoke OpenCode CLI tools.
    - `_run_shell_command` ensures the correct agent's API key and model are used for each OpenCode CLI call.
- **System Prompts for Tooling:** `system_prompt_ceo.txt` and `system_prompt_genius.txt` were updated to include explicit instructions and examples for using OpenCode CLI tools, guiding the models' behavior.
- **Simplified Conversation Loop:** `main.py` was refactored to remove threading and implement a sequential, turn-based conversation for clarity and easier debugging.
- **Conversation Logging:** Implemented a `Tee` class in `main.py` to log all console output to a timestamped file in the `conversations/` directory.
- **Error Handling:** Addressed `TypeError` in `main.py` related to `run_turn` arguments.
- **Instructions File:** Confirmed `instructions.txt` is dynamically read for the mission, not hardcoded.

## Current State
The framework is set up for sequential agent conversation with OpenCode CLI integration, distinct agent personalities, and conversation logging. The primary remaining task is to ensure the agents effectively utilize the OpenCode CLI tools based on their system prompts and the given instructions.

## Next Steps
- Test the full loop with the corrected OpenCode CLI invocations and system prompts.
- Observe agent behavior and refine system prompts/logic as needed for effective tool use and collaboration.
- Further develop the self-improvement mechanisms.
