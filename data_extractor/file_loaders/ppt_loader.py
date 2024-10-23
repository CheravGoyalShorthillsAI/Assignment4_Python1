from pptx import Presentation
from data_extractor.file_loaders.file_loader import FileLoader
from data_extractor.file_loaders.loaderHelper import LoaderHelper

class PPTLoader(FileLoader):
    def load_file(self, file_path: str) -> Presentation:
        return LoaderHelper(file_path, Presentation).load()