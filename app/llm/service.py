from pydantic import BaseModel

from app.llm.base import LLMProvider


class LLMService:
    """Application-facing service for LLM operations."""

    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[BaseModel],
    ) -> BaseModel:
        return await self._provider.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=response_model,
        )