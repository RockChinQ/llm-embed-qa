import openai

from ...models.llm import adapter


class OpenAIGPT(adapter.LLMAdapter):
    
    model: str
    
    def __init__(self, model: str, **kwargs):
        self.model = model

    def ask(self, messages: list) -> str:
        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        
        return resp['choices'][0]['message']['content']
