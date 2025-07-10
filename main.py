from app.email_client import EmailClient
from app.summarize import summarize_text
from app.categoriser import categorize_email
from app.auto_reply import generate_reply
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    logging.info(f"Smart Email Assistant started.")

    client = EmailClient()
    try :
        client.login()
        logging.info("Logged in successfully!")
    except Exception as e:
        logging.error(f"Failed to login: {e}")
        return

    emails = client.fetch_unread_emails()
    if not emails:
        logging.info("No unread emails found.")
        return
    
    for email in emails :
        logging.info(f"Processing email from: {email['from']} — Subject: {email['subject']}")
        
        summary = summarize_text(email["body"])
        logging.info(f"Summary:{summary}")
        
        category = categorize_email(email["body"])
        logging.info(f"Category: {category}")
        
        reply = generate_reply(email["body"], category)   
        
        try:
            client.send_email(email["from"], f"Re: {email['subject']}", reply)
            logging.info("Reply sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send reply: {e}")
        
    logging.info ("All Emails processed")

if __name__== "__main__":
    main()