import openai
from app.config_loader import load_config
import logging, os

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'app.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

config = load_config()
openai.api_key = config["OPENAI_API_KEY"]
MODEL_NAME = config["OPENAI_MODEL"]

logging.basicConfig(level=logging.INFO, format= "%(asctime)s - %(levelname)s - %(message)s")

def summarize_text(text):
    try : 
        logging.info("Summarizing Email content...")
        
        response = openai.ChatCompletion.create(
            model = MODEL_NAME,
            messages = [
                {"role": "system", "content": "Summarize the following email."},
                {"role": "user", "content": text}
            ],
        temperature = 0.5,
        max_tokens = 150
        )
        
        summary = response['choice'][0]['message']['content']
        logging.info("Summary generated successfully")
        return summary
    
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        
    except Exception as e :
        logging.error(f"Unexpected error during the summarzation {e}")
        return "[Error: Unexpected issue while summarizing.]"
    