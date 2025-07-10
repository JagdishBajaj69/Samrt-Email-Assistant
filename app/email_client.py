import imaplib
import smtplib
import email
import logging, os
from email.mime.text import MIMEText
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

config  = load_config()

class EmailClient:
    def __init__(self):
        self.email_address = config["GMAIL_EMAIL"]
        self.password = config["GMAIL_APP_PASSWORD"]
        
        try: 
            self.imap = imaplib.IMAP4_SSL("imap.gmail.com")
            self.smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            logging.info("IMAP and SMTP connection created successfully")
        
        except Exception as e:
            logging.info(f"Failed to create Email-Client connection: {e}")
            
    def login(self):
        try:
            self.imap.login(self.email_address, self.password)
            self.smtp.login(self.email_address, self.password)
            logging.info("logged into Gmail successfully.")
        except imaplib.IMAP4.error as e:
            logging.info(f"Failed to login to IMAP: {e}")
            raise
        except smtplib.SMTPAuthenticationError as e:
            logging.info(f"Failed to login to SMTP: {e}")
            raise
        except Exception as e:
            logging.info(f"Unexpected logging error: {e}")
            raise
    
    def fetch_unread_emails(self):
        try:
            self.imap.select("inbox")
            _, messages = self.imap.search(None, 'UNSEEN')
            email_list = []

            for num in messages[0].split():
                _, data = self.imap.fetch(num, '(RFC822)')
                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = msg.get("subject", "No Subject")
                sender = msg.get("from", "Unknown Sender")
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                body = "[Unreadable Body]"
                                logging.warning("Failed to decode multipart text/plain part.")
                else:
                    try:
                        body = msg.get_payload(decode=True).decode()
                    except:
                        body = "[Unreadable Body]"
                        logging.warning("Failed to decode single-part email body.")

                email_list.append({
                    "subject": subject,
                    "from": sender,
                    "body": body
                }) 
            logging.info(f"Fetched {len(email_list)} unread email(s).")
            return email_list

        except Exception as e:
            logging.error(f"Error fetching emails: {e}")
            return []

    def send_email(self, to_address, subject, message):
        try:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = self.email_address
            msg["To"] = to_address
            
            self.smtp.sendmail(self.email_address, to_address, msg.as_string())
            logging.info(f"sent email to {to_address} with subject '{subject}'.")
        except Exception as e:
            logging.error(f"Error sending email to {to_address}: {e}")