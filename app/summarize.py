import google.generativeai as genai
from app.config_loader import load_config
import logging


config = load_config()
genai.configure (api_key = config["GEMINI_API_KEY"])
MODEL_NAME = config["GEMINI_MODEL"]

logging.basicConfig(level=logging.INFO, format= "%(asctime)s - %(levelname)s - %(message)s")

def summarize_text(text):
    try : 
        logging.info("Summarizing Email content...")
        
        model = genai.GenerativeModel(MODEL_NAME)
        chat = model.start_chat()
        response = chat.send_message(f"Summarize the following email:\n\n{text}")
        summary = response.text
        logging.info("Summary generated successfully")
        text = response.text.strip()
        return summary
        
    except Exception as e :
        logging.error(f"Unexpected error during the summarization :{e}")
        return "[Error: Unexpected issue while summarizing.]"
    