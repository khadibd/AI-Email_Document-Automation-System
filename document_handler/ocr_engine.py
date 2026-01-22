import easyocr
from pdf2image import convert_from_path
from PIL import Image
import logging


class OCREngine:
    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)

    def extract_text(self, file_path):
        text = ""

        try:
            if file_path.lower().endswith(".pdf"):
                images = convert_from_path(file_path)
                for img in images:
                    text += self._ocr_image(img)
            else:
                image = Image.open(file_path)
                text += self._ocr_image(image)

        except Exception as e:
            logging.error(f"OCR failed for {file_path}: {e}")
            raise

        return text

    def _ocr_image(self, image):
        results = self.reader.readtext(image)
        return " ".join([r[1] for r in results])
