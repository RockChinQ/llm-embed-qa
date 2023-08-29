import numpy as np
import openai

from ...models.embedding import embedding
from ...control import factory


@factory.component(embedding.EmbeddingProvider, "openai")
class OpenAIEmbedding(embedding.EmbeddingProvider):
    """Get embedding from OpenAI API."""

    model: str
    api_key: str

    def __init__(self, model: str, api_key: str, **kwargs):
        self.model = model
        self.api_key = api_key

    def get_embedding(self, text: str) -> np.ndarray:
        openai.api_key = self.api_key

        resp = openai.Embedding.create(
            input=text,
            model=self.model
        )

        return np.array(resp['data'][0]['embedding'])

    def get_dim(self) -> int:
        """Returns the dimension of the embedding."""
        return 1536
