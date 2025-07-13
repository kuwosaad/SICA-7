import os
from openai import OpenAI
import subprocess
import json
import time
from pathlib import Path
import queue
import threading

class Agent:
    def __init__(self, name, role, comm_queue, openrouter_model, api_key=None):
        self.name = name
        self.role = role
        self.comm_queue = comm_queue
        self.openrouter_model = openrouter_model
        self.openrouter_api_key = api_key # Use the provided API key
        self.workspace_dir = Path("/Users/mohammadsaad/Desktop/SICA/SICA 7/two-agent-framework/sandbox")
        self.workspace_dir.mkdir(exist_ok=True)
        
        # No direct OpenAI client here; interaction is via OpenCode CLI
        self.messages = [] # Still useful for local tracking of conversation flow

    def send_message(self, recipient_agent, message_content):
        print(f"\n{self.name} sent a message to {recipient_agent.name}.") # Concise confirmation
        recipient_agent.comm_queue.put((self.name, message_content))

    def receive_message(self):
        try:
            sender, message = self.comm_queue.get(timeout=10) # Wait for message
            self.messages.append({"role": "user", "content": message}) # Add to own history
            return sender, message
        except queue.Empty:
            return None, None

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def _run_shell_command(self, cmd_list, cwd=None, timeout=120):
        """Internal helper to run shell commands."""
        env = os.environ.copy()
        env['OPENROUTER_API_KEY'] = self.openrouter_api_key # Ensure API key is in env
        
        try:
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                env=env,
                cwd=str(cwd if cwd else self.workspace_dir),
                timeout=timeout
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'model_used': self.openrouter_model
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False, 
                'error': 'Command execution timed out',
                'model_used': self.openrouter_model
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': f"Command not found: {cmd_list[0]}. Ensure it's in your PATH.",
                'model_used': self.openrouter_model
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"An error occurred: {e}",
                'model_used': self.openrouter_model
            }

    def opencode_run_prompt(self, prompt, session_id=None):
        """Send a prompt to the OpenCode CLI agent for conversational interaction."""
        cmd = [
            'opencode', 'run',
            '-m', f"openrouter/{self.openrouter_model}",
            prompt # Pass prompt as positional argument
        ]
        if session_id:
            cmd.extend(['--session', session_id])
        return self._run_shell_command(cmd)

    def opencode_view_file(self, file_path):
        """View the contents of a file using OpenCode CLI."""
        cmd = [
            'opencode', 'view',
            file_path
        ]
        return self._run_shell_command(cmd)

    def opencode_edit_file(self, file_path, description):
        """Edit a file using OpenCode CLI with a description of changes."""
        cmd = [
            'opencode', 'edit',
            file_path,
            '--description', description
        ]
        return self._run_shell_command(cmd)

    def opencode_write_file(self, file_path, content):
        """Write content to a new file using OpenCode CLI."""
        cmd = [
            'opencode', 'write',
            file_path,
            '--content', content
        ]
        return self._run_shell_command(cmd)

    def opencode_bash_command(self, command):
        """Execute a bash command using OpenCode CLI."""
        cmd = [
            'opencode', 'bash',
            command
        ]
        return self._run_shell_command(cmd)

    def reflect_and_improve(self, task_success, state_file="agent_state.json"):
        """Enhanced reflection with OpenCode-driven improvements"""
        state_file_path = self.workspace_dir / state_file
        try:
            with open(state_file_path, "r") as f:
                state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            state = {
                "upgrades": [],
                "success_rate": 1.0,
                "capabilities": [],
                "model_used": self.openrouter_model
            }
        
        # Update success rate
        current_successes = len([u for u in state["upgrades"] if u.get("successful", True)])
        total_attempts = len(state["upgrades"]) + 1
        state["success_rate"] = (current_successes + (1 if task_success else 0)) / total_attempts
        
        # Trigger improvements if success rate drops below threshold
        if not task_success or state["success_rate"] < 0.8:
            improvement_prompt = f"""
            Analyze my current capabilities and suggest improvements.
            Current success rate: {state['success_rate']:.2f}
            Last task success: {task_success}
            Available tools: OpenCode CLI, file operations, shell commands
            Suggest specific code improvements or new tool integrations.
            """
            
            # Use opencode_run_prompt for reflection
            improvement_result = self.opencode_run_prompt(improvement_prompt)
            
            if improvement_result['success']:
                # Implement the suggested improvement (this part needs careful design)
                # For now, we'll just log the suggestion
                print(f"\n{self.name} suggests improvement: {improvement_result['output']}")
                state["upgrades"].append({
                    "timestamp": time.time(),
                    "suggestion": improvement_result['output'],
                    "successful": True # Assume success for now, actual implementation is complex
                })
            else:
                print(f"\n{self.name} failed to suggest improvement: {improvement_result['error']}")
                state["upgrades"].append({
                    "timestamp": time.time(),
                    "suggestion": "Failed to generate improvement",
                    "successful": False
                })
        
        # Save updated state
        with open(state_file_path, "w") as f:
            json.dump(state, f, indent=2)
