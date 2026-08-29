class AegisError(Exception):
    """Base exception for expected Aegis application errors."""


class ConfigurationError(AegisError):
    """Raised when application configuration is invalid."""


class LLMError(AegisError):
    """Raised when an LLM operation fails."""


class ToolError(AegisError):
    """Raised when a tool execution fails."""


class RetrievalError(AegisError):
    """Raised when knowledge retrieval fails."""


class EvidenceError(AegisError):
    """Raised when evidence processing fails."""


class DecisionError(AegisError):
    """Raised when decision processing fails."""