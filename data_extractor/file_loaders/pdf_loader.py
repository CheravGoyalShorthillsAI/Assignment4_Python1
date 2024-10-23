from PyPDF2 import PdfReader
from data_extractor.file_loaders.file_loader import FileLoader
from data_extractor.file_loaders.loaderHelper import LoaderHelper

class PDFLoader(FileLoader):
    def load_file(self, file_path: str) -> PdfReader:
        return LoaderHelper(file_path, PdfReader).load()