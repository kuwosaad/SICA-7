import os
import subprocess
import queue
import threading
import time
import json
import sys
import re
from datetime import datetime

from agent import Agent
from config import AGENT1_API_KEY, AGENT2_API_KEY, AGENT1_MODEL, AGENT2_MODEL, OPENCODE_WORKSPACE

# Custom stdout class to tee output to console and file
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # Ensure immediate write
    def flush(self):
        for f in self.files:
            f.flush()

# Function to extract tool code from agent's response
def extract_tool_code(response_content):
    tool_code_pattern = re.compile(r'<\|tool calls begin\|><\|tool call begin\|>function<\|tool sep\|>(.*?)(?:<\|tool call end\|>)?<\|tool calls end\|>', re.DOTALL)
    match = tool_code_pattern.search(response_content)
    if match:
        # Extract the content within the tool call block
        tool_call_content = match.group(1).strip()
        
        # Remove the tool call block from the original response
        cleaned_response = tool_code_pattern.sub('', response_content).strip()
        
        # The tool call content might contain the command and then JSON arguments
        # We need to parse this carefully.
        # Example: opencode run\n```json\n{"prompt": "..."}\n```
        
        # Split by newline to separate command from JSON (if any)
        parts = tool_call_content.split('\n```json\n', 1)
        command_line = parts[0].strip()
        json_args = None
        if len(parts) > 1:
            json_block = parts[1].strip()
            if json_block.endswith('\n```'):
                json_block = json_block[:-len('\n```')].strip()
            try:
                json_args = json.loads(json_block)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse JSON arguments for tool call: {json_block}")
                json_args = None
        
        return cleaned_response, command_line, json_args
    return response_content, None, None

class Alpha(Agent):
    def __init__(self, name, role, comm_queue, openrouter_model, system_prompt=None, api_key=None):
        super().__init__(name, role, comm_queue, openrouter_model, api_key=api_key) # Corrected super().__init__ call
        self.system_prompt = system_prompt # Store system prompt for initial message

    def run_turn(self, recipient_agent, message_to_process):
        # Alpha's turn to process and send a message
        print(f"\n{self.name} is thinking...")
        
        # Prepend system prompt to the first message
        if not self.messages and self.system_prompt:
            message_to_process = f"{self.system_prompt}\n\n{message_to_process}"

        # Use opencode_run_prompt for conversational interaction
        opencode_response = self.opencode_run_prompt(message_to_process)
        
        if opencode_response['success']:
            raw_response = opencode_response['output']
            cleaned_response, tool_command, tool_args = extract_tool_code(raw_response)
            
            print(f"\n{self.name}: {cleaned_response}")
            
            if tool_command:
                print(f"\n{self.name} is executing tool: {tool_command} with args: {tool_args}")
                tool_output = {'success': False, 'output': 'No tool executed.', 'error': ''}
                
                # Execute the tool command based on its type
                if tool_command.startswith("opencode run"): # Conversational prompt
                    prompt = tool_args.get("prompt", "") if tool_args else ""
                    tool_output = self.opencode_run_prompt(prompt)
                elif tool_command.startswith("opencode view"): # View file
                    file_path = tool_command.split(" ", 2)[2].strip() # Extract file_path
                    tool_output = self.opencode_view_file(file_path)
                elif tool_command.startswith("opencode write"): # Write file
                    file_path = tool_args.get("file_path", "") if tool_args else ""
                    content = tool_args.get("content", "") if tool_args else ""
                    tool_output = self.opencode_write_file(file_path, content)
                elif tool_command.startswith("opencode bash"): # Bash command
                    command = tool_command.split(" ", 2)[2].strip() # Extract command
                    tool_output = self.opencode_bash_command(command)
                # Add more tool types as needed

                if tool_output['success']:
                    print(f"\nTool Output (Success):\n{tool_output['output']}")
                    self.add_message("tool_output", tool_output['output'])
                    self.send_message(recipient_agent, f"Tool executed successfully. Output: {tool_output['output']}")
                else:
                    print(f"\nTool Output (Error):\n{tool_output['error']}")
                    self.add_message("tool_error", tool_output['error'])
                    self.send_message(recipient_agent, f"Tool execution failed. Error: {tool_output['error']}")
            else:
                self.send_message(recipient_agent, cleaned_response)
        else:
            print(f"\n{self.name} (OpenCode Error): {opencode_response['error']}")
            self.send_message(recipient_agent, f"OpenCode execution failed: {opencode_response['error']}")

class Beta(Agent):
    def __init__(self, name, role, comm_queue, openrouter_model, system_prompt=None, api_key=None):
        super().__init__(name, role, comm_queue, openrouter_model, api_key=api_key) # Corrected super().__init__ call
        self.system_prompt = system_prompt # Store system prompt for initial message

    def run_turn(self, recipient_agent, message_to_process):
        print(f"\n{self.name} is thinking...")

        # Prepend system prompt to the first message
        if not self.messages and self.system_prompt:
            message_to_process = f"{self.system_prompt}\n\n{message_to_process}"

        # Use opencode_run_prompt for conversational interaction
        opencode_response = self.opencode_run_prompt(message_to_process)

        if opencode_response['success']:
            raw_response = opencode_response['output']
            cleaned_response, tool_command, tool_args = extract_tool_code(raw_response)

            print(f"\n{self.name}: {cleaned_response}")

            if tool_command:
                print(f"\n{self.name} is executing tool: {tool_command} with args: {tool_args}")
                tool_output = {'success': False, 'output': 'No tool executed.', 'error': ''}
                
                # Execute the tool command based on its type
                if tool_command.startswith("opencode run"): # Conversational prompt
                    prompt = tool_args.get("prompt", "") if tool_args else ""
                    tool_output = self.opencode_run_prompt(prompt)
                elif tool_command.startswith("opencode view"): # View file
                    file_path = tool_command.split(" ", 2)[2].strip() # Extract file_path
                    tool_output = self.opencode_view_file(file_path)
                elif tool_command.startswith("opencode write"): # Write file
                    file_path = tool_args.get("file_path", "") if tool_args else ""
                    content = tool_args.get("content", "") if tool_args else ""
                    tool_output = self.opencode_write_file(file_path, content)
                elif tool_command.startswith("opencode bash"): # Bash command
                    command = tool_command.split(" ", 2)[2].strip() # Extract command
                    tool_output = self.opencode_bash_command(command)
                # Add more tool types as needed

                if tool_output['success']:
                    print(f"\nTool Output (Success):\n{tool_output['output']}")
                    self.add_message("tool_output", tool_output['output'])
                    self.send_message(recipient_agent, f"Tool executed successfully. Output: {tool_output['output']}")
                else:
                    print(f"\nTool Output (Error):\n{tool_output['error']}")
                    self.add_message("tool_error", tool_output['error'])
                    self.send_message(recipient_agent, f"Tool execution failed. Error: {tool_output['error']}")
            else:
                self.send_message(recipient_agent, cleaned_response)
        else:
            print(f"\n{self.name} (OpenCode Error): {opencode_response['error']}")
            self.send_message(recipient_agent, f"OpenCode execution failed: {opencode_response['error']}")

def assess_cycle_performance(alpha, beta):
    """Assess whether the current cycle was successful"""
    # Implement success metrics based on your specific criteria
    # For now, return True for basic implementation
    return True

def setup_opencode_cli():
    """Install and configure OpenCode CLI if not present"""
    try:
        # Check if OpenCode CLI is installed
        result = subprocess.run(['opencode', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Installing OpenCode CLI...")
            subprocess.run([
                'curl', '-fsSL', 
                'https://raw.githubusercontent.com/opencode-ai/opencode/refs/heads/main/install'
            ], shell=True, check=True) # Added check=True to raise error on failure
        
        # Configure authentication
        api_key = os.getenv('AGENT1_API_KEY') # Use AGENT1_API_KEY for opencode auth
        if api_key:
            print("Configuring OpenCode CLI authentication...")
            # OpenCode CLI auth login expects input on stdin
            process = subprocess.Popen(['opencode', 'auth', 'login', 'openrouter'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(input=api_key)
            if process.returncode != 0:
                print(f"OpenCode CLI authentication failed: {stderr}")
                return False
            print(f"OpenCode CLI authentication output: {stdout}")
        
        print("OpenCode CLI setup complete.")
        return True
    except FileNotFoundError:
        print("'opencode' command not found. Please ensure OpenCode CLI is in your PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"OpenCode CLI installation failed: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"OpenCode CLI setup failed: {e}")
        return False

def main():
    # Setup logging to file and console
    log_dir = os.path.join(os.path.dirname(__file__), "conversations")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(log_dir, f"conversation_{timestamp}.log")
    
    original_stdout = sys.stdout
    log_file = open(log_filename, "w")
    sys.stdout = Tee(original_stdout, log_file)

    try:
        comm_queue_alpha = queue.Queue() # Queue for Alpha to receive messages
        comm_queue_beta = queue.Queue()  # Queue for Beta to receive messages
        
        # Read system prompts
        ceo_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt_ceo.txt")
        genius_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt_genius.txt")

        try:
            with open(ceo_prompt_path, "r") as f:
                ceo_system_prompt = f.read().strip()
        except FileNotFoundError:
            ceo_system_prompt = None

        try:
            with open(genius_prompt_path, "r") as f:
                genius_system_prompt = f.read().strip()
        except FileNotFoundError:
            genius_system_prompt = None

        # Create model-aligned agents with their respective API keys
        alpha = Alpha("Agent1 (Alpha)", "Planner", comm_queue_alpha, AGENT1_MODEL, system_prompt=ceo_system_prompt, api_key=AGENT1_API_KEY)
        beta = Beta("Agent2 (Beta)", "Executor", comm_queue_beta, AGENT2_MODEL, system_prompt=genius_system_prompt, api_key=AGENT2_API_KEY)
        
        # Load initial instructions
        instructions_file_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
        try:
            with open(instructions_file_path, "r") as f:
                initial_instructions = f.read().strip()
        except FileNotFoundError:
            initial_instructions = "No instructions found. Agents will start a general conversation."
        
        print(f"\nInitial Instruction for Agents:\n{initial_instructions}\n")

        # Sequential conversation loop
        for cycle in range(1): # Limiting to 1 cycle for initial testing
            print(f"\n=== Cycle {cycle + 1} ===")
            
            # Alpha starts the conversation
            alpha.run_turn(beta, initial_instructions) # Alpha sends message to Beta

            # Beta receives and responds
            sender, msg = beta.receive_message()
            if msg: # Only proceed if a message was received
                beta.run_turn(alpha, msg) # Beta sends message to Alpha

            # Alpha receives and responds
            sender, msg = alpha.receive_message()
            if msg: # Only proceed if a message was received
                alpha.run_turn(beta, msg) # Alpha sends message to Beta

            # Beta receives and responds (final turn for this cycle)
            sender, msg = beta.receive_message()
            if msg: # Only proceed if a message was received
                beta.run_turn(alpha, msg) # Beta sends message to Alpha

            # Performance assessment for self-improvement
            task_success = assess_cycle_performance(alpha, beta)
            alpha.reflect_and_improve(task_success)
            beta.reflect_and_improve(task_success)

        print("\nInteraction complete.")

    finally:
        # Restore original stdout and close log file
        sys.stdout = original_stdout
        log_file.close()

if __name__ == "__main__":
    if setup_opencode_cli():
        main()
    else:
        print("Failed to setup OpenCode CLI. Please install manually.")