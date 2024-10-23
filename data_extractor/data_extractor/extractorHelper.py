from data_extractor.data_extractor.iterator import FileExtractorIterator

class ExtractData():
    def __init__(self, file_path):
        self.file_path = file_path
    
    def extractData(self):
        # get the file type
        file_iterator = FileExtractorIterator(self.file_path)
        
        try:
            extractor = next(file_iterator)
            # Use the extractor as needed
        except StopIteration:
            raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")
        
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