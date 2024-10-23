from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader

class ExtractData():
    def __init__(self, file_path):
        self.file_path = file_path
    
    def get_extractor(self):
        # Manually create a list of supported extensions and their respective classes
        supported_extensions = {
            ".pdf": (PDFLoader, PDFExtractor),
            ".docx": (DOCXLoader, DOCXExtractor),
            ".pptx": (PPTLoader, PPTXExtractor),
            ".ppt": (PPTLoader, PPTXExtractor),
        }
        
        # Check the file extension and return the corresponding extractor
        for extension, (loader_class, extractor_class) in supported_extensions.items():
            if self.file_path.endswith(extension):
                try:
                    loader = loader_class()
                    extractor = extractor_class(loader, self.file_path)
                    return extractor
                except Exception as e:
                    print(f"Error initializing extractor for {self.file_path}: {e}")
                    return None
        
        raise ValueError(f"Unsupported file type: {self.file_path}")
    
    def extractData(self):
        # get the file type
        extractor= self.get_extractor()
        
        #extract texts 
        extracted_text = extractor.extract_text()

        # Extract images
        extracted_images = extractor.extract_images()
        
        # Extract URLs
        extracted_urls = extractor.extract_urls()

        # Extract tables
        extractor_tables = extractor.extract_tables()
        
        # return a dictionary of items extracted
        return {
            "text": extracted_text,
            "images": extracted_images,
            "urls": extracted_urls,
            "tables": extractor_tables}