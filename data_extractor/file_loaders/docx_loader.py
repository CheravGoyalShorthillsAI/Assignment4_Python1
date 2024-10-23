from docx import Document
from data_extractor.file_loaders.file_loader import FileLoader
from data_extractor.file_loaders.loaderHelper import LoaderHelper

class DOCXLoader(FileLoader):
    def load_file(self, file_path: str) -> Document:
        return LoaderHelper(file_path, Document).load()