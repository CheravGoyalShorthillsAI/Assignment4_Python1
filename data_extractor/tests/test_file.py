import pytest
import os
from data_extractor.data_extractor.extractorHelper import ExtractData
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage


loader = PDFLoader()
# Load a valid file format
def test_load_valid_file():
    
    assert loader.load_file('test_files/pdf/Sample_file.pdf')

# Load a file till the maximum allowed size
def test_load_max_size_file():
    
    assert loader.load_file('test_files/pdf/large.pdf')

# Load a file with special characters in the filename
def test_load_special_chars_file():
    
    assert loader.load_file('test_files/pdf/@@chinese.pdf')

# Load a file with UTF-8 encoding
def test_load_utf8_file():
    
    assert loader.load_file('test_files/pdf/unstandard_language.pdf')

# Load a file with password protected files
def test_load_password_protected_file():
    
    assert loader.load_file('test_files/pdf/sample-protected.pdf')

# Load file with unusual text fonts and styles
def test_load_unusual_fonts_file():
    
    assert loader.load_file('test_files/pdf/unstandard_language.pdf')

# Load a file with embedded media (audio, video)
def test_load_embedded_media_file():
    
    assert loader.load_file('test_files/pdf/Sample_file.pdf')

# Load file with rotated pages
def test_load_rotated_pages_file():
    
    assert loader.load_file('test_files/pdf/Sample_file.pdf')

# Load an unsupported file format
def test_load_unsupported_file():
    with pytest.raises(ValueError):
        loader.load_file('test_files/pdf/Data_Extractor_Overview.txt')

# Load a corrupted file
def test_load_corrupted_file(): 
    
    with pytest.raises(ValueError): 
        loader.load_file('test_files/pdf/corrupt.pdf')

# Load a file exceeding the maximum allowed size
def test_load_exceeds_max_size_file():
    
    assert loader.load_file('test_files/pdf/large.pdf')

# Load an empty file (0 bytes)
def test_load_empty_file():
    
    assert loader.load_file('test_files/pdf/empty.pdf')

# Test if load_file raises FileNotFoundError
def test_load_file_not_found():
    
    with pytest.raises(ValueError):
        loader.load_file('test_files/pdf/non_existent.pdf')

# Extract text from a file containing only text
def test_extract_text():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Aman_resume.pdf')
    assert extractor.extract_text()

# Extract images from a file containing only images
def test_extract_images():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/small.pdf')
    assert extractor.extract_images()

# Extract URLs from a file containing only URLs
def test_extract_urls():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Aman_resume.pdf')
    assert extractor.extract_urls()

# Define the test files
test_files = {
    'valid_file': 'valid_file.pdf',
    'table_only_file': 'table_only.pdf',
}

# Extract tables from a file containing only tables.
def test_extract_tables_from_table_only_file():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Sample_file.pdf')
    tables = extractor.extract_tables()
    assert len(tables) > 0
    for table in tables:
        assert len(table) > 0

# Extract mixed content (text, images, URLs, tables) from a file.
def test_extract_mixed_content_from_valid_file():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Sample_file.pdf')
    data = {'text': extractor.extract_text(), 'images': extractor.extract_images(), 'urls': extractor.extract_urls(), 'tables': extractor.extract_tables()}
    assert 'text' in data
    assert 'images' in data
    assert 'urls' in data
    assert 'tables' in data

# Extract formatted text and verify formatting is preserved.
def test_extract_formatted_text_from_valid_file():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/A.pdf')
    text = extractor.extract_text()
    assert '**bold text**' in text
    assert '*italic text*' in text

# Attempt to extract content from a file with password protection
def test_extract_from_password_protected_file():
    loader = PDFLoader()
    # with pytest.raises(Exception):
    assert loader.load_file('test_files/pdf/sample-protected.pdf')
        # loader.load_file('test_files/pdf/sample-protected.pdf')

# Handle files with partial data corruption (e.g., half-loaded images).
def test_extract_from_partially_corrupted_file():
    loader = PDFLoader()
    with pytest.raises(Exception): 
        loader.load_file('test_files/pdf/corrupt.pdf')

# Extract content from a password-protected or encrypted file.
def test_extract_from_encrypted_file():
    loader = PDFLoader()
    # with pytest.raises(Exception):
    #     loader.load_file('test_files/pdf/sample-protected.pdf')
    assert loader.load_file('test_files/pdf/sample-protected.pdf')

# Handle files with broken or malformed structures (e.g., incomplete tables).
def test_extract_from_broken_structure_file():
    loader = PDFLoader()
    # with pytest.raises(Exception):
    #     loader.load_file('test_files/pdf/unstandard_language.pdf')
    assert loader.load_file('test_files/pdf/unstandard_language.pdf')

# Create a directory with the file's name.
def test_create_directory_with_file_name():
    file_name = 'test_files/pdf/@@chinese.pdf'
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    print('\n\n\n\n\n','base name - - - - ', base_name,'\n\n\n\n\n')
    output_dir = os.path.join("extracted_data", base_name)
    

    extractor = PDFExtractor(PDFLoader(), file_name)
    data = {'text': extractor.extract_text(), 'images': extractor.extract_images(), 'urls': extractor.extract_urls(), 'tables': extractor.extract_tables()}


    storage = FileStorage(output_dir)
    
    storage.store(data['images'], file_name, 'image')/home/shtlp_0046/Desktop/Assignment_4_python_UPDATED/data_extractor/tests/test_file.py
    storage.store(data['text'], file_name, 'text')
    storage.store(data['urls'], file_name, 'url')
    storage.store(data['tables'], file_name, 'data_table')


    assert os.path.exists(os.path.join(output_dir, 'images'))
    assert os.path.exists(os.path.join(output_dir, 'text'))
    assert os.path.exists(os.path.join(output_dir, 'url'))
    assert os.path.exists(os.path.join(output_dir, 'data_table'))

# Save extracted text to the appropriate directory.
def test_save_text():
    file_name = 'test_files/pdf/Aman_resume.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    text = extractor.extract_text()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)

    storage = FileStorage(output_dir)
    storage.save_text(text, file_name)

    assert os.path.exists(os.path.join(output_dir, ))

# Save images in the 'image' directory.
def test_save_images():
    
    file_name = 'test_files/pdf/Sample_file.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    images = extractor.extract_images()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    storage.save_images(images, file_name)


    assert os.path.exists(os.path.join(output_dir, file_name))

# Save tables in the 'table' directory.
def test_save_tables():
    file_name = 'test_files/pdf/Sample_file.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    tables = extractor.extract_tables()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    storage.save_tables(tables, file_name)


    assert os.path.exists(os.path.join(output_dir, file_name))

# Save tables in the 'text' directory.
def test_save_tables_in_text_dir():
    file_name = 'test_files/pdf/Sample_file.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    tables = extractor.extract_tables()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    storage.save_tables(tables, file_name, dir_name='text')

    assert os.path.exists(os.path.join(output_dir, file_name, 'text', 'tables'))

# Save tables in the 'url' directory.
def test_save_tables_in_url_dir():
    file_name = 'test_files/pdf/Sample_file.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    tables = extractor.extract_urls()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    storage.save_tables(tables, file_name, dir_name='url')
    assert os.path.exists(os.path.join(output_dir, file_name, 'url', 'tables'))

# Attempt to save content to a non-existent directory.
def test_save_to_non_existent_dir():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/non_existent.pdf')
    text = extractor.extract_text()
    storage = FileStorage('non_existent_dir')
    with pytest.raises(FileNotFoundError):
        storage.save_text(text, 'test_files/pdf/non_existent.pdf')

# Handle scenarios where saving fails due to disk space limitations.
def test_save_fails_due_to_disk_space():
    file_name = 'test_files/pdf/large.pdf'
    extractor = PDFExtractor(PDFLoader(), file_name)
    text = extractor.extract_text()
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    # simulate disk space limitation
    with pytest.raises(IOError):
        storage.save_text(text, file_name)

# Simulate a failure during directory creation (e.g., permissions issue).
def test_create_dir_fails_due_to_permissions():
    file_name = 'test_file.pdf'
    
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    output_dir = os.path.join("extracted_data", base_name)


    storage = FileStorage(output_dir)
    # simulate permissions issue
    with pytest.raises(PermissionError):
        storage.create_directory(file_name)

# Attempt to save to the database when the connection is down.
def test_save_to_db_when_connection_down():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Sample_file.pdf')
    text = extractor.extract_text()
    storage = SQLStorage('non_existent_db')
    with pytest.raises(ConnectionError):
        storage.save_text('text', text, 'test_files/pdf/Sample_file.pdf')

# Handle error when storing to invalid SQL DB
def test_save_to_invalid_sql_db():
    extractor = PDFExtractor(PDFLoader(), 'test_files/pdf/Sample_file.pdf')
    text = extractor.extract_text()
    storage = SQLStorage('invalid_db')
    with pytest.raises(ValueError):
        storage.store('text', text, 'test_files/pdf/Sample_file.pdf')
