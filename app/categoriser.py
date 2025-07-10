import google.generativeai as genai
import logging
from app.config_loader import load_config

config = load_config()
genai.configure(api_key = config["GEMINI_API_KEY"])
model_name  = config["GEMINI_MODEL"]

logging.basicConfig(level= logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def categorize_email(text):
    try: 
        logging.info("Categorizing Email...")
        
        prompt = (
                "You are an email urgency classifier. Categorize the following email as strictly one of these: "
                "'Urgent', 'Normal', or 'Spam'.\n\n"
                "Only reply with one of the following words: Urgent, Normal, or Spam. No explanation."
            )
        model = genai.GenerativeModel(model_name)
        chat = model.start_chat()
        response = chat.send_message(f"{prompt}\n\n{text}")
        category = response.text.strip()
        
        for label in ["urgent", "normal", "spam"]:
            if label in category:
                category = label.capitalize()
                break
        else:
            category = "Unknown"

        logging.info(f"Email categorized as {category}")
        logging.info(f"Raw Gemini response: {response.text}")
        return category
    
    except Exception as e:
        logging.error(f"Unexpected error during categorization: {e}")
        return "Unknown"