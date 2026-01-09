"""Base interface for AI coding tool adapters.

All tool adapters (Aider, Goose, etc.) must implement this interface
to ensure consistent behavior across the SDLC pipeline.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class Complexity(Enum):
    """Task complexity levels with associated timeouts."""

    SIMPLE = "simple"  # 30s timeout, single file, straightforward change
    MEDIUM = "medium"  # 60s timeout, multi-file, logic changes
    COMPLEX = "complex"  # 120s timeout, refactoring, architecture changes


class ModelProvider(Enum):
    """Supported model providers."""

    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    LOCAL = "local"  # LMStudio, Ollama


@dataclass
class ToolConfig:
    """Configuration for a tool adapter.

    Attributes:
        model: Model identifier (e.g., "claude-3-5-haiku-latest", "qwen/qwen3-30b")
        provider: Model provider (anthropic, openai, local)
        timeout_seconds: Max execution time
        max_retries: Number of retry attempts on failure
        working_dir: Directory for tool execution
        env_vars: Additional environment variables
    """

    model: str
    provider: ModelProvider
    timeout_seconds: int = 60
    max_retries: int = 2
    working_dir: Path | None = None
    env_vars: dict[str, str] = field(default_factory=dict)

    @classmethod
    def for_complexity(cls, complexity: Complexity, **kwargs: Any) -> "ToolConfig":
        """Create config with timeout based on complexity."""
        timeouts = {
            Complexity.SIMPLE: 30,
            Complexity.MEDIUM: 60,
            Complexity.COMPLEX: 120,
        }
        return cls(timeout_seconds=timeouts[complexity], **kwargs)


@dataclass
class ExecutionResult:
    """Result of a tool execution.

    Attributes:
        success: Whether the execution completed successfully
        output: Tool output (stdout, generated content)
        error: Error message if failed
        files_modified: List of files that were changed
        tokens_used: Number of tokens consumed (for cost tracking)
        execution_time_seconds: How long the execution took
        match_percentage: Quality score (0-100) if validation was performed
    """

    success: bool
    output: str
    error: str | None = None
    files_modified: list[str] = field(default_factory=list)
    tokens_used: int = 0
    execution_time_seconds: float = 0.0
    match_percentage: float | None = None

    @property
    def cost_estimate(self) -> float:
        """Estimate cost based on tokens used (Haiku pricing ~$0.25/1M input)."""
        if self.tokens_used == 0:
            return 0.0
        # Rough estimate: $0.25 per 1M input tokens, $1.25 per 1M output tokens
        # Assume 70% input, 30% output
        input_cost = (self.tokens_used * 0.7) * 0.00000025
        output_cost = (self.tokens_used * 0.3) * 0.00000125
        return input_cost + output_cost


class ToolAdapter(ABC):
    """Abstract base class for AI coding tool adapters.

    All adapters must implement:
    - execute(): Run the tool with a prompt and files
    - validate_output(): Check if the output meets quality standards
    - get_cost(): Return the cost of the last execution

    Example usage:
        adapter = AiderAdapter(config)
        result = await adapter.execute(
            prompt="Fix the null pointer exception in utils.py",
            files=["src/utils.py"]
        )
        if result.success:
            is_valid = await adapter.validate_output(result)
    """

    def __init__(self, config: ToolConfig) -> None:
        """Initialize adapter with configuration."""
        self.config = config
        self._last_result: ExecutionResult | None = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the adapter name (e.g., 'aider', 'goose')."""
        ...

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the tool version."""
        ...

    @abstractmethod
    async def execute(
        self,
        prompt: str,
        files: list[str] | None = None,
        context: str | None = None,
    ) -> ExecutionResult:
        """Execute the tool with the given prompt.

        Args:
            prompt: The task description or instruction
            files: List of file paths to operate on
            context: Additional context (e.g., from Repomix)

        Returns:
            ExecutionResult with success status, output, and metadata
        """
        ...

    @abstractmethod
    async def validate_output(self, result: ExecutionResult) -> bool:
        """Validate the execution output.

        Checks:
        - Syntax: Code compiles/parses
        - Semantic: Tests pass (if applicable)
        - Style: Linting passes

        Args:
            result: The execution result to validate

        Returns:
            True if output is valid, False otherwise
        """
        ...

    def get_cost(self) -> float:
        """Get the estimated cost of the last execution."""
        if self._last_result is None:
            return 0.0
        return self._last_result.cost_estimate

    async def health_check(self) -> bool:
        """Check if the tool is available and configured correctly."""
        return True  # Override in subclasses for actual checks

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.config.model})"
