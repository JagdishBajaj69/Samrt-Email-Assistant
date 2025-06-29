from app.config_loader import load_config
import openai

config = load_config()

openai.api_key = config["openai_api_key"]

# Now you can use OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Summarize this email"}]
)

print(response['choices'][0]['message']['content'])
