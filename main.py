import os
import json
import logging
import sqlite3
import pandas as pd

from email_handler.email_reader import EmailReader
from email_handler.email_sender import EmailSender

from document_handler.ocr_engine import OCREngine
from text_processing.text_cleaner import TextCleaner

from ai_processing.classifier import DocumentClassifier
from ai_processing.invoice_extractor import InvoiceExtractor
from ai_processing.llm_extractor import LLMExtractor

from config import TEXT_DIR, RESULTS_DIR, LOG_DIR, DB_DIR


# Logging setup
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(os.path.join(DB_DIR, "results.db"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file TEXT,
            type TEXT,
            amount TEXT,
            date TEXT,
            invoice_number TEXT,
            sender_email TEXT
        )
    """)
    conn.commit()
    return conn


def save_to_db(conn, data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO invoices (file, type, amount, date, invoice_number, sender_email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("file"),
        data.get("type"),
        data.get("amount"),
        data.get("date"),
        data.get("invoice_number"),
        data.get("sender_email")
    ))
    conn.commit()


def export_to_excel(results):
    if not results:
        logging.warning("No results to export to Excel.")
        return

    df = pd.DataFrame(results)
    df.to_excel(os.path.join("data", "results.xlsx"), index=False)
    logging.info("Excel exported successfully.")


def main():
    logging.info("Pipeline started")

    documents = []
    try:
        documents = EmailReader().fetch_emails()
    except Exception as e:
        logging.error(f"Email fetch failed: {e}")

    os.makedirs(TEXT_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    ocr = OCREngine()
    cleaner = TextCleaner()
    classifier = DocumentClassifier()
    extractor = InvoiceExtractor()
    llm_extractor = LLMExtractor()
    sender = EmailSender()

    conn = init_db()

    all_results = []

    for doc in documents:
        file = doc["file_path"]
        sender_email = doc["sender_email"]

        try:
            raw_text = ocr.extract_text(file)
            clean_text = cleaner.clean(raw_text)

            doc_type = classifier.classify(clean_text)

            result = {
                "file": os.path.basename(file),
                "type": doc_type,
                "sender_email": sender_email,
                "amount": None,
                "date": None,
                "invoice_number": None
            }

            if doc_type == "invoice":
                invoice_data = extractor.extract(clean_text)
                llm_data = llm_extractor.extract(clean_text)

                # Merge data
                result.update(invoice_data)
                result.update(llm_data)

            json_path = os.path.join(RESULTS_DIR, os.path.basename(file) + ".json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4)

            logging.info(f"Processed {file} as {doc_type}")

            save_to_db(conn, result)
            all_results.append(result)

            sender.send_reply(
                to_email=sender_email,
                subject=f"Document Processed: {os.path.basename(file)}",
                body=f"Hello,\n\nYour document {os.path.basename(file)} has been processed.\n\nResult:\n{json.dumps(result, indent=2)}\n\nThank you."
            )

        except Exception as e:
            logging.error(f"Failed processing {file}: {e}")
            continue

    export_to_excel(all_results)
    logging.info("Pipeline finished")


if __name__ == "__main__":
    main()
