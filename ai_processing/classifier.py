class DocumentClassifier:
    def classify(self, text):
        text_lower = text.lower()

        if "invoice" in text_lower or "total" in text_lower:
            return "invoice"
        if "contract" in text_lower:
            return "contract"
        return "unknown"
