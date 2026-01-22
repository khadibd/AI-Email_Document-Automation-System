import openai
import logging
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


class LLMExtractor:
    def extract(self, text):
        try:
            prompt = f"""
            Extract invoice fields from this text:
            - invoice_number
            - date
            - amount
            - vendor_name

            Text:
            {text}
            """

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an invoice extractor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )

            return response["choices"][0]["message"]["content"].strip()

        except Exception as e:
            logging.error(f"LLM extraction failed: {e}")
            return None
