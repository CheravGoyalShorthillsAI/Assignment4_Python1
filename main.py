import os

from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.info_extractor.docx_extractor import DOCXExtractor
from data_extractor.info_extractor.pdf_extractor import PDFExtractor
from data_extractor.info_extractor.pptx_extractor import PPTXExtractor
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage

def main():
    """
    Main function for extracting data from a file.

    This function takes a file path as an argument, determines the file type (PDF, DOCX, or PPTX),
    uses the appropriate loader to validate and load the file, creates an instance of DataExtractor
    to extract content, and then saves the extracted data to a folder and a SQL database.

    Parameters:
        file_path (str): Path to the file to be processed

    Returns:
        None
    """
    file_path = "/home/shtlp_0046/Desktop/Assignment4/files/Networks 1.pptx"  

    # Determine the file type and use the appropriate loader
    if file_path.endswith(".pdf"):
        loader = PDFLoader()
        extractor = PDFExtractor(loader)
    elif file_path.endswith(".docx"):
        loader = DOCXLoader()
        extractor = DOCXExtractor(loader)
    elif file_path.endswith(".pptx") or file_path.endswith(".ppt"):
        loader = PPTLoader()
        extractor = PPTXExtractor(loader)
    else:
        raise ValueError("Unsupported file format. Use PDF, DOCX, or PPTX.")

    # Extract text from the file
    extractor.load(file_path)
    extracted_text = extractor.extract_text()
    # print(extracted_text)

    # Extract images (if available)
    images = extractor.extract_images()

    # Extract URLs (if it's a PDF or DOCX)
    urls = extractor.extract_urls() 
    # print(urls)

    # Extract tables (for PDFs or DOCX only)
    tables = extractor.extract_tables()

    # Create a folder for storing the extracted data
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    output_dir = os.path.join("extracted_data", base_name)
    file_storage = FileStorage(output_dir)

    # Save the extracted text
    file_storage.store(extracted_text, os.path.basename(file_path), 'text')

    # Save the extracted images
    image_data=None
    if images:
        image_data = file_storage.store(images, os.path.basename(file_path), 'image')

    # Save the extracted URLs (if any)
    if urls:
        file_storage.store(urls, os.path.basename(file_path), 'url')

    # Save the extracted tables (if any)
    if tables:
        file_storage.store(tables, os.path.basename(file_path), 'table')

    print(f"Extracted data saved to: {output_dir}")
    
    # Create an instance of SQLStorage
    sql_storage = SQLStorage('assignment4.db')

    # Store the extracted text in the SQL database
    sql_storage.store("text", extracted_text)

    # Store the extracted images in the SQL database
    if images:
        sql_storage.store("image", image_data)

    # Store the extracted URLs in the SQL database
    if urls:
        sql_storage.store("url", urls)

    # Store the extracted tables in the SQL database
    if tables:
        for table in tables:
            sql_storage.store("data_table", table)

    print("Data stored in SQL database")
    sql_storage.close()
    # loader.close_file()

if __name__ == "__main__":
    main()
