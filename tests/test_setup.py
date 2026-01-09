"""Basic tests to verify project setup."""


def test_imports() -> None:
    """Test that all packages can be imported."""
    from src import __version__
    from src.adapters import ExecutionResult, ToolAdapter, ToolConfig
    from src.adapters.base.interface import Complexity, ModelProvider

    assert __version__ == "0.1.0"
    assert ToolAdapter is not None
    assert ExecutionResult is not None
    assert ToolConfig is not None
    assert Complexity.SIMPLE.value == "simple"
    assert ModelProvider.ANTHROPIC.value == "anthropic"


def test_execution_result_cost() -> None:
    """Test ExecutionResult cost calculation."""
    from src.adapters import ExecutionResult

    # No tokens = no cost
    result = ExecutionResult(success=True, output="test", tokens_used=0)
    assert result.cost_estimate == 0.0

    # With tokens
    result = ExecutionResult(success=True, output="test", tokens_used=1000)
    assert result.cost_estimate > 0


def test_tool_config_for_complexity() -> None:
    """Test ToolConfig factory method."""
    from src.adapters import ToolConfig
    from src.adapters.base.interface import Complexity, ModelProvider

    config = ToolConfig.for_complexity(
        Complexity.SIMPLE,
        model="claude-3-5-haiku-latest",
        provider=ModelProvider.ANTHROPIC,
    )
    assert config.timeout_seconds == 30

    config = ToolConfig.for_complexity(
        Complexity.COMPLEX,
        model="claude-sonnet-4-20250514",
        provider=ModelProvider.ANTHROPIC,
    )
    assert config.timeout_seconds == 120
