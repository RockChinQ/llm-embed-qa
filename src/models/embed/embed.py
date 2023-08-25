import numpy as np


class EmbeddingProvider:
    
    def __init__(self, **kwargs):
        pass
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Returns the embedding of the text.
        
        Args:
            text: The text to embed, search key of a document.
        """
        pass
