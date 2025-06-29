import yaml
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)



'''
Add this in every file : 

from app.config_loader import load_config

config = load_config()
openai_api_key = config['openai_api_key']

'''