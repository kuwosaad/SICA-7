import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file located in the same directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

AGENT1_API_KEY = os.getenv('AGENT1_API_KEY')
AGENT2_API_KEY = os.getenv('AGENT2_API_KEY')
AGENT1_MODEL = os.getenv('AGENT1_MODEL', 'deepseek/deepseek-r1-0528:free')
AGENT2_MODEL = os.getenv('AGENT2_MODEL', 'deepseek/deepseek-r1-0528-qwen3-8b:free')
OPENCODE_WORKSPACE = os.getenv('OPENCODE_WORKSPACE', 'sandbox')
