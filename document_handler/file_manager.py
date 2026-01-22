import os
from config import SUPPORTED_EXTENSIONS


class FileManager:
    def get_documents(self, directory):
        return [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if any(f.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)
        ]
