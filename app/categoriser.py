import openai
import logging
from app.config_loader import load_config

config = load_config()
openai.api_key = config["OPENAI_API_KEY"]
model_name  = config["MODEL_NAME"]

logging.basicConfig(level= logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def categorize_email(text):
    try: 
        logging.info("Categorizing Email...")
        
        prompt = (
            "Categorize the email as one of the following: "
            "[Urgent, Normal, Spam]. Reply with the only category name."
        )
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            max_tokens=10  # We only expect one word back
        )
        category = response['choice'][0]['message']['content'].strip()
        logging.info(f"Email categorized as {category}")
        return category
    
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error during categorization: {e}")
        return "Unknown"
    
    except Exception as e:
        logging.error(f"Unexpected error during categorization: {e}")
        return "Unknown"