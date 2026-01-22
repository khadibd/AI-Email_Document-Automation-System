import re


class TextCleaner:
    def clean(self, text):
        text = re.sub(r"\s+", " ", text)
        return text.strip()
