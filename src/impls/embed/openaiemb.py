
import numpy as np
import openai

from ...models.embed import embed


class OpenAIEmbedding(embed.EmbeddingProvider):
    
    model: str
    
    def __init__(self, model: str, **kwargs):
        self.model = model
        
    def get_embedding(self, text: str) -> np.array:
        resp = openai.Embedding.create(
            input=text,
            model=self.model
        )
        
        return np.array(resp['data'][0]['embedding'])
        