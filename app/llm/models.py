from pydantic import BaseModel, Field


class LLMUsage(BaseModel):
    """Token usage returned by an LLM invocation."""

    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)


class LLMResponse[T](BaseModel):
    """Generic structured LLM response with usage metadata."""

    output: T
    usage: LLMUsage