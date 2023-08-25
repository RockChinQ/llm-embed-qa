import numpy as np

class Document:
    """A document."""

    name: str
    """Name of the document."""

    key: str
    """Search key of the document."""

    embedding: np.ndarray
    """Vector embedding of the document."""

    content: str
    """Content of the document."""

    digest: str
    """Digest of the document content."""
