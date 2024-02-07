from dataclasses import dataclass, asdict
from typing import Literal
import json

from openai import AsyncOpenAI
from reminder.config import load_config

cfg = load_config()

@dataclass
class ChatMessage:
    role: Literal['system', 'user', 'assistant']
    content: str


class OpenAIChatLLM:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.0
    ):
        self.client = AsyncOpenAI(api_key=api_key)

        self.model_kwargs = {
            'model': model,
            'temperature': temperature
        }

    async def apredict_json(self, messages: list[ChatMessage]) -> dict:
        extra_params = {}
        if self.model_kwargs['model'] == 'gpt-3.5-turbo':
            extra_params['response_format'] = {'type': 'json_object'}
        
        resp = await self.client.chat.completions.create(
            messages=[asdict(message) for message in messages], **self.model_kwargs
        )
        resp_content = resp.choices[0].message.content
        resp_content = self.response_to_dict(text=resp_content)
        return resp_content
    
    def response_to_dict(self, text: str) -> dict:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return Exception("Invalid LLM JSON Response")


chat_llm = OpenAIChatLLM(
    api_key=cfg.openai.api_key,
    model=cfg.openai.model
)