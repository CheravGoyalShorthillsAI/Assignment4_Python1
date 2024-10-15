import os
from PyPDF2 import PdfReader

from data_extractor.file_loaders.file_loader import FileLoader


class PDFLoader(FileLoader):

    def validate_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pdf')

    def load_file(self, file_path: str) -> PdfReader:
        if not self.validate_file(file_path):
            raise ValueError("Invalid PDF file.")
        return PdfReader(file_path)
