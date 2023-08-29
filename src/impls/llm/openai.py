import openai

from ...models.llm import adapter
from ...control import factory


@factory.component(adapter.LLMAdapter, "openai")
class OpenAIGPT(adapter.LLMAdapter):
    """Get response from OpenAI API."""

    model: str
    api_key: str

    def __init__(self, model: str, api_key: str, **kwargs):
        self.model = model
        self.api_key = api_key

    def ask(self, messages: list) -> str:
        openai.api_key = self.api_key

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )

        return resp['choices'][0]['message']['content']
