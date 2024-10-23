from abc import ABC, abstractmethod
from typing import Any

class FileLoader(ABC):
    @abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass