import re


class InvoiceExtractor:
    def extract(self, text):
        return {
            "amount": self._extract_amount(text),
            "date": self._extract_date(text),
            "invoice_number": self._extract_invoice_number(text)
        }

    def _extract_amount(self, text):
        match = re.search(r"(total|amount)\s*[:\-]?\s*\$?\s*(\d+[\.,]?\d*)", text, re.I)
        return match.group(2) if match else None

    def _extract_date(self, text):
        match = re.search(r"\b(\d{2}/\d{2}/\d{4})\b", text)
        return match.group(1) if match else None

    def _extract_invoice_number(self, text):
        match = re.search(r"(invoice\s*no\.?|invoice\s*#)\s*[:\-]?\s*(\w+)", text, re.I)
        return match.group(2) if match else None
