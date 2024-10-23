from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader

class FileExtractorIterator:
        def __init__(self, file_path):
            self.file_path = file_path
            self.supported_extensions = [
                (".pdf", PDFLoader, PDFExtractor),
                (".docx", DOCXLoader, DOCXExtractor),
                (".pptx", PPTLoader, PPTXExtractor),
                (".ppt", PPTLoader, PPTXExtractor)
            ]
            self.index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.supported_extensions):
                raise StopIteration
            
            extension, loader_class, extractor_class = self.supported_extensions[self.index]
            self.index += 1
            
            if self.file_path.endswith(extension):
                loader = loader_class()
                extractor = extractor_class(loader, self.file_path)
                return extractor
            
            # If current extension doesn't match, continue to the next one
            return self.__next__()