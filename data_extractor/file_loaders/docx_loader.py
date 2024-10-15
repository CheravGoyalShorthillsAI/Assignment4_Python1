import docx

from data_extractor.file_loaders.file_loader import FileLoader


class DOCXLoader(FileLoader):

    def validate_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.docx')

    def load_file(self, file_path: str) -> docx.Document:
        if not self.validate_file(file_path):
            raise ValueError("Invalid DOCX file.")
        return docx.Document(file_path)
    

