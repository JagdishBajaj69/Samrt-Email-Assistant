import google.generativeai as genai
import logging
from app.config_loader import load_config

config = load_config()
genai.configure(api_key=config["GEMINI_API_KEY"])
model_name = config["GEMINI_MODEL"]

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

        model = genai.GenerativeModel(model_name)
        prompt = f"{base_prompt}\n\nReply to this email:\n\n{email_text}"
        chat = model.start_chat()
        response = chat.send_message(prompt, generation_config={"max_output_tokens": 350})
        
        reply = response.text.strip()
        
        logging.info("Auto reply generated successfully!")
        return reply
    
    except Exception as e:
        logging.error(f"Unexpected error occurred during reply generation: {e}")
        return "[Error: Unexpected issue while generating reply.: {e}]"
    