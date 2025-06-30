import openai
import logging, os
from app.config_loader import load_config

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
model_name = config["OPENAI_MODEL"]
open_api_key = config["OPENAI_API_KEY"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_reply(email_text, category):
    try:
        logging.info(f"Generating auto-reply according to category...")
       
        if category.lower() == "spam":
            logging.info (f"Email classified as spam. Skipping reply")
            return None
        
        base_prompt = "You are helpful and polite email assistant"
        if category.lower() == "urgent":
            base_prompt += " The email is urgent. Make sure your reply is quick and clearly addresses the concern according to the tone of email."
        else:
            base_prompt += " Respond in a professional and friendly tone."

        response = openai.ChatCompletion.create(
            model = model_name,
            message = [
                {"role": "system", "content":base_prompt},
                {"role": "user", "content": f"Reply to this email:\n\n{email_text}"}
            ],
            temperature = 0.6,
            max_token = 200
        )
        
        reply = response['choice'][0]['message']['content'].strip()
        logging.info("Auto reply generated successfully!")
        return reply
    
    except openai.error.OpenAIError as e:
        logging.info("OpenAI API error during genterating reply:{e} ")
        return "[Error: Could not generate auto-reply.]"
    
    except Exception as e:
        logging.info(f"Unexpected error occurred during reply generation: {e}")
        return "[Error: Unexpected issue while generating reply.]"
    