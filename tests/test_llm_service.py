import pytest
from pydantic import BaseModel

from app.llm.base import LLMProvider
from app.llm.service import LLMService


class TestOutput(BaseModel):
    answer: str


class FakeLLMProvider(LLMProvider):
    async def generate_structured(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_model: type[TestOutput],
    ) -> TestOutput:
        return response_model(answer="fake response")


@pytest.mark.asyncio
async def test_llm_service_uses_provider():
    provider = FakeLLMProvider()
    service = LLMService(provider)

    result = await service.generate_structured(
        system_prompt="You are a test assistant.",
        user_prompt="Say hello.",
        response_model=TestOutput,
    )

    assert result.answer == "fake response"