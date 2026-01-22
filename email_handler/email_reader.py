import os
import logging
from imapclient import IMAPClient
import pyzmail
from config import EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD, DOCUMENT_DIR, FILTER_KEYWORDS


class EmailReader:
    def fetch_emails(self):
        logging.info("Connecting to email server")

        documents = []

        with IMAPClient(EMAIL_HOST) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.select_folder("INBOX")

            # Fetch UNSEEN emails only
            messages = server.search(["UNSEEN"])
            logging.info(f"Found {len(messages)} new emails")

            for uid in messages:
                raw = server.fetch(uid, ["BODY[]"])
                message = pyzmail.PyzMessage.factory(raw[uid][b"BODY[]"])

                subject = message.get_subject() or ""
                from_email = message.get_addresses("from")[0][1]

                # Filter by keywords
                if not self._is_relevant(subject):
                    server.add_flags(uid, [b"\\Seen"])
                    continue

                # Save attachments
                for part in message.mailparts:
                    if part.filename:
                        file_path = self._save_attachment(part)
                        documents.append({
                            "file_path": file_path,
                            "sender_email": from_email
                        })

                # MARK AS SEEN after processing
                server.add_flags(uid, [b"\\Seen"])
                logging.info(f"Email processed: {subject} from {from_email}")

        return documents

    def _save_attachment(self, part):
        os.makedirs(DOCUMENT_DIR, exist_ok=True)
        path = os.path.join(DOCUMENT_DIR, part.filename)

        with open(path, "wb") as f:
            f.write(part.get_payload())

        logging.info(f"Attachment saved: {part.filename}")
        return path

    def _is_relevant(self, subject):
        subject_lower = subject.lower()
        return any(k in subject_lower for k in FILTER_KEYWORDS)
