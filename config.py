# config.py

import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = "imap.gmail.com"
EMAIL_USER = os.getenv("your_e-mail")
EMAIL_PASSWORD = os.getenv("your_password")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SUPPORTED_EXTENSIONS = [".pdf", ".png", ".jpg", ".jpeg"]

BASE_DIR = "data"
DOCUMENT_DIR = os.path.join(BASE_DIR, "documents")
TEXT_DIR = os.path.join(BASE_DIR, "extracted_text")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
LOG_DIR = "logs"
DB_DIR = "db"

FILTER_KEYWORDS = ["invoice", "receipt", "bill"]