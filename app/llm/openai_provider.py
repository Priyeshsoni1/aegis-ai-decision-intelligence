from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.llm.base import LLMProvider


T = TypeVar("T", bound=BaseModel)


class OpenAIProvider(LLMProvider):
    """OpenAI implementation of the LLM provider."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str,
        timeout: float = 30.0,
    ) -> None:
        self._client = AsyncOpenAI(
            api_key=api_key,
            timeout=timeout,
        )
        self._model = model

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[T],
    ) -> T:
        response = await self._client.responses.parse(
            model=self._model,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            text_format=response_model,
        )

        if response.output_parsed is None:
            raise RuntimeError(
                "OpenAI returned no structured output."
            )

        return response.output_parsed