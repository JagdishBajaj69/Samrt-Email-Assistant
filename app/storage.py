import os
import csv
import logging

# Path to store processed email records
STORAGE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'replied_emails.csv')

# Ensure directory exists
os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)

def load_processed_emails():
    """
    Loads the list of already replied-to emails from storage.
    Returns a set of identifiers (Message-ID or fallback).
    """
    processed = set()
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    if row:
                        processed.add(row[0])
        except Exception as e:
            logging.error(f"Error reading storage file: {e}")
    return processed

def save_processed_email(email_id):
    """
    Saves a processed email ID to the storage file.
    """
    try:
        file_exists = os.path.isfile(STORAGE_FILE)
        with open(STORAGE_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['email_id'])  # header
            writer.writerow([email_id])
        logging.info(f"Stored processed email ID: {email_id}")
    except Exception as e:
        logging.error(f"Error writing to storage file: {e}")
