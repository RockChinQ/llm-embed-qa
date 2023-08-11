
import numpy as np
import openai

from ...models.embed import embed


class OpenAIEmbedding(embed.EmbeddingProvider):
    
    model: str
    api_key: str
    
    def __init__(self, model: str, api_key: str, **kwargs):
        self.model = model
        self.api_key = api_key
        
    def get_embedding(self, text: str) -> np.array:
        openai.api_key = self.api_key
        
        resp = openai.Embedding.create(
            input=text,
            model=self.model
        )
        
        return np.array(resp['data'][0]['embedding'])
        