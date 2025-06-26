import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from project.agent_core import run_agent
from project.config_manager import load_config

if __name__ == "__main__":
    config = load_config()
    run_agent(config)
