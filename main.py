from app.email_client import EmailClient
from app.summarize import summarize_text
from app.categoriser import categorize_email
from app.auto_reply import generate_reply
from app.storage import load_processed_emails, save_processed_email
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
processed_emails = load_processed_emails()

def main():
    logging.info("Smart Email Assistant started.")

    client = EmailClient()
    try:
        client.login()
        logging.info("Logged in successfully!")
    except Exception as e:
        logging.error(f"Failed to login: {e}")
        return

    emails = client.fetch_unread_emails()
    if not emails:
        logging.info("No unread emails found.")
        return

    for email in emails:
        email_id = email.get("message_id") or f"{email['subject']}_{email['from']}"
        if email_id in processed_emails:
            logging.info("Email already processed. Skipping.")
            continue

        logging.info(f"Processing email from: {email['from']} — Subject: {email['subject']}")

        summary = summarize_text(email["body"])
        logging.info(f"Summary: {summary}")

        category = categorize_email(email["body"])
        logging.info(f"Category: {category}")

        reply = generate_reply(email["body"], category)

        if reply is None:
            logging.info("Skipping spam or unknown category email.")
            continue

        try:
            client.send_email(email["from"], f"Re: {email['subject']}", reply)
            logging.info("Reply sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send reply: {e}")
            continue  # Don't mark it as processed if reply failed

        save_processed_email(email_id)

    logging.info("All Emails processed.")

if __name__ == "__main__":
    main()
