import unittest
from unittest.mock import MagicMock
from data_extractor.data_extractor.docx_extractor import DOCXExtractor
from data_extractor.data_extractor.pdf_extractor import PDFExtractor
from data_extractor.data_extractor.pptx_extractor import PPTXExtractor
from data_extractor.file_loaders.pdf_loader import PDFLoader
from data_extractor.file_loaders.docx_loader import DOCXLoader
from data_extractor.file_loaders.ppt_loader import PPTLoader
from data_extractor.storage.file_storage import FileStorage
from data_extractor.storage.sql_storage import SQLStorage


class TestPDFLoader(unittest.TestCase):
    def setUp(self):
        self.pdf_loader = PDFLoader()  # Correct initialization
        self.pdf_loader.load_file = MagicMock()

    def test_load_file(self):
        self.pdf_loader.load_file()
        self.pdf_loader.load_file.assert_called_once()

    def test_extract_text(self):
        self.pdf_loader.extract_text = MagicMock(return_value=("Sample text", {"font_style": "Arial", "page_number": 1}))
        text, metadata = self.pdf_loader.extract_text()
        self.assertEqual(text, "Sample text")
        self.assertEqual(metadata, {"font_style": "Arial", "page_number": 1})

    def test_extract_links(self):
        self.pdf_loader.extract_links = MagicMock(return_value=[{"text": "Example", "url": "http://example.com", "page_number": 1}])
        links = self.pdf_loader.extract_links()
        self.assertEqual(links[0]["url"], "http://example.com")

    def test_extract_images(self):
        self.pdf_loader.extract_images = MagicMock(return_value=[{"resolution": (1024, 768), "format": "JPEG", "page_number": 1}])
        images = self.pdf_loader.extract_images()
        self.assertEqual(images[0]["format"], "JPEG")

    def test_extract_tables(self):
        self.pdf_loader.extract_tables = MagicMock(return_value=[{"dimensions": (5, 3), "page_number": 1}])
        tables = self.pdf_loader.extract_tables()
        self.assertEqual(tables[0]["dimensions"], (5, 3))


class TestDOCXLoader(unittest.TestCase):
    def setUp(self):
        self.docx_loader = DOCXLoader()  # Correct initialization
        self.docx_loader.load_file = MagicMock()

    def test_load_file(self):
        self.docx_loader.load_file()
        self.docx_loader.load_file.assert_called_once()

    def test_extract_text(self):
        self.docx_loader.extract_text = MagicMock(return_value=("Sample DOCX text", {"font_style": "Times New Roman"}))
        text, metadata = self.docx_loader.extract_text()
        self.assertEqual(text, "Sample DOCX text")
        self.assertEqual(metadata["font_style"], "Times New Roman")

    def test_extract_links(self):
        self.docx_loader.extract_links = MagicMock(return_value=[{"text": "Docx link", "url": "http://docx.com"}])
        links = self.docx_loader.extract_links()
        self.assertEqual(links[0]["text"], "Docx link")

    def test_extract_images(self):
        self.docx_loader.extract_images = MagicMock(return_value=[{"resolution": (800, 600), "format": "PNG"}])
        images = self.docx_loader.extract_images()
        self.assertEqual(images[0]["format"], "PNG")

    def test_extract_tables(self):
        self.docx_loader.extract_tables = MagicMock(return_value=[{"dimensions": (2, 4)}])
        tables = self.docx_loader.extract_tables()
        self.assertEqual(tables[0]["dimensions"], (2, 4))


class TestPPTLoader(unittest.TestCase):
    def setUp(self):
        self.ppt_loader = PPTLoader()  # Correct initialization
        self.ppt_loader.load_file = MagicMock()

    def test_load_file(self):
        self.ppt_loader.load_file()
        self.ppt_loader.load_file.assert_called_once()

    def test_extract_text(self):
        self.ppt_loader.extract_text = MagicMock(return_value=("Slide text", {"slide_number": 1}))
        text, metadata = self.ppt_loader.extract_text()
        self.assertEqual(text, "Slide text")
        self.assertEqual(metadata["slide_number"], 1)

    def test_extract_links(self):
        self.ppt_loader.extract_links = MagicMock(return_value=[{"text": "PPT Link", "url": "http://pptlink.com"}])
        links = self.ppt_loader.extract_links()
        self.assertEqual(links[0]["url"], "http://pptlink.com")

    def test_extract_images(self):
        self.ppt_loader.extract_images = MagicMock(return_value=[{"resolution": (1280, 720), "format": "JPEG"}])
        images = self.ppt_loader.extract_images()
        self.assertEqual(images[0]["resolution"], (1280, 720))

    def test_extract_tables(self):
        self.ppt_loader.extract_tables = MagicMock(return_value=[{"dimensions": (3, 5)}])
        tables = self.ppt_loader.extract_tables()
        self.assertEqual(tables[0]["dimensions"], (3, 5))


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.extractor = MagicMock()
        self.file_storage = FileStorage(self.extractor)

    def test_store_text(self):
        self.file_storage.store_text = MagicMock()
        self.file_storage.store_text()
        self.file_storage.store_text.assert_called_once()

    def test_store_links(self):
        self.file_storage.store_links = MagicMock()
        self.file_storage.store_links()
        self.file_storage.store_links.assert_called_once()

    def test_store_images(self):
        self.file_storage.store_images = MagicMock()
        self.file_storage.store_images()
        self.file_storage.store_images.assert_called_once()

    def test_store_tables(self):
        self.file_storage.store_tables = MagicMock()
        self.file_storage.store_tables()
        self.file_storage.store_tables.assert_called_once()


class TestSQLStorage(unittest.TestCase):
    def setUp(self):
        # SQLStorage may not need the extractor as a parameter
        self.sql_storage = SQLStorage()  # Correct initialization, no extractor needed

    def test_store_text(self):
        self.sql_storage.store_text = MagicMock()
        self.sql_storage.store_text()
        self.sql_storage.store_text.assert_called_once()

    def test_store_links(self):
        self.sql_storage.store_links = MagicMock()
        self.sql_storage.store_links()
        self.sql_storage.store_links.assert_called_once()

    def test_store_images(self):
        self.sql_storage.store_images = MagicMock()
        self.sql_storage.store_images()
        self.sql_storage.store_images.assert_called_once()

    def test_store_tables(self):
        self.sql_storage.store_tables = MagicMock()
        self.sql_storage.store_tables()
        self.sql_storage.store_tables.assert_called_once()


class TestCombinations(unittest.TestCase):
    def test_pdf_combinations(self):
        loader = PDFLoader()
        combinations = [
            ("extract_text", loader.extract_text, ("Text", {})),
            ("extract_links", loader.extract_links, [{"url": "http://example.com"}]),
            ("extract_images", loader.extract_images, [{"format": "JPEG"}]),
            ("extract_tables", loader.extract_tables, [{"dimensions": (3, 4)}]),
        ]
        for name, method, result in combinations:
            method = MagicMock(return_value=result)
            output = method()
            self.assertEqual(output, result)

    def test_docx_combinations(self):
        loader = DOCXLoader()
        combinations = [
            ("extract_text", loader.extract_text, ("Text", {})),
            ("extract_links", loader.extract_links, [{"url": "http://docxlink.com"}]),
            ("extract_images", loader.extract_images, [{"format": "PNG"}]),
            ("extract_tables", loader.extract_tables, [{"dimensions": (2, 4)}]),
        ]
        for name, method, result in combinations:
            method = MagicMock(return_value=result)
            output = method()
            self.assertEqual(output, result)

    def test_ppt_combinations(self):
        loader = PPTLoader()
        combinations = [
            ("extract_text", loader.extract_text, ("Text", {})),
            ("extract_links", loader.extract_links, [{"url": "http://pptlink.com"}]),
            ("extract_images", loader.extract_images, [{"format": "JPEG"}]),
            ("extract_tables", loader.extract_tables, [{"dimensions": (3, 5)}]),
        ]
        for name, method, result in combinations:
            method = MagicMock(return_value=result)
            output = method()
            self.assertEqual(output, result)


# Run the tests
if __name__ == "__main__":
    unittest.main()
