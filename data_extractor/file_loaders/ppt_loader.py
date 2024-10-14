import pptx
from data_extractor.file_loaders.file_loader import FileLoader

class PPTLoader(FileLoader):
    
    def validate_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.pptx') or file_path.lower().endswith('.ppt')

    def load_file(self, file_path: str) -> pptx.Presentation:
        if not self.validate_file(file_path):
            raise ValueError("Invalid PPT file.")
        return pptx.Presentation(file_path)
    
  