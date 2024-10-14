from typing import Any, Dict, List
from data_extractor.data_extractor.extractor import Extractor

class DOCXExtractor(Extractor):
    def __init__(self, loader):
        self.loader = loader
        self.file = None
        self.file_path = None

    def load(self, file_path):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path

    def extract_text(self):
        """Extract text from paragraphs and tables in the DOCX file."""
        text = ""

        # Extract text from paragraphs
        for paragraph in self.file.paragraphs:
            text += paragraph.text + "\n"

        # Extract text from tables
        for table in self.file.tables:
            for row in table.rows:
                row_text = "\t".join(cell.text.strip() for cell in row.cells)
                text += row_text + "\n"

        return text

    def extract_images(self):
        """Extract images from the DOCX file."""
        images = []

        for rel in self.file.part.rels.values():
            if "image" in rel.target_ref:
                image_blob = rel.target_part.blob
                # Get the image extension
                image_ext = rel.target_part.content_type.split('/')[1]
                if image_blob:
                    images.append({
                        "image_data": image_blob,
                        "ext": image_ext
                    })

        return images

    def extract_urls(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a DOCX file."""
        extracted_links = []

        for rel in self.file.part.rels.values():
            if "hyperlink" in rel.reltype:
                hyperlink = rel.target_ref
                linked_text = None
                page_number = None
                for para_index, para in enumerate(self.file.paragraphs, start=1):
                    for run in para.runs:
                        if hyperlink in run._element.xml:
                            linked_text = run.text
                            page_number = para_index
                            break
                    if linked_text:
                        break
                
                extracted_links.append({
                    "linked_text": linked_text or "",
                    "url": hyperlink,
                    "page_number": page_number
                })

        return extracted_links

    def extract_tables(self):
        """Extract tables from DOCX."""
        table_data = []
        for table in self.file.tables:
            table_content = [[cell.text.strip() for cell in row.cells] for row in table.rows]
            table_data.append(table_content)

        return table_data
