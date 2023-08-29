import numpy as np

from .. import entities


class DatabaseManager:
    
    def __init__(self, **kwargs):
        pass
    
    def del_all(self):
        pass
    
    def store(self, docs: list[entities.Document]):
        """Stores the document(with embedding set)."""
        pass
    
    def exists(self, name: str) -> bool:
        """Returns whether the document exists."""
        pass

    def check(self, name: str, digest: str) -> bool:
        """Returns whether the document exists and its digest matches."""
        pass

    def delete(self, name: str):
        """Deletes the document."""
        pass
    
    def search(self, embedding: np.ndarray) -> list[entities.Document]:
        pass
    