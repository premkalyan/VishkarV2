"""Tests to validate CI/CD workflow configuration."""

from pathlib import Path

import yaml

WORKFLOWS_DIR = Path(__file__).parent.parent / ".github" / "workflows"


def test_workflows_directory_exists() -> None:
    """Test that workflows directory exists."""
    assert WORKFLOWS_DIR.exists(), f"Workflows directory not found at {WORKFLOWS_DIR}"


def test_ci_workflow_exists() -> None:
    """Test that CI workflow file exists."""
    ci_workflow = WORKFLOWS_DIR / "ci.yml"
    assert ci_workflow.exists(), "ci.yml workflow not found"


def test_pr_workflow_exists() -> None:
    """Test that PR workflow file exists."""
    pr_workflow = WORKFLOWS_DIR / "pr.yml"
    assert pr_workflow.exists(), "pr.yml workflow not found"


def test_ci_workflow_valid_yaml() -> None:
    """Test that CI workflow is valid YAML."""
    ci_workflow = WORKFLOWS_DIR / "ci.yml"
    with open(ci_workflow) as f:
        workflow = yaml.safe_load(f)

    assert "name" in workflow
    # YAML parses 'on:' as boolean True, so check for True key
    assert True in workflow or "on" in workflow
    assert "jobs" in workflow


def test_ci_workflow_has_required_jobs() -> None:
    """Test that CI workflow has all required jobs."""
    ci_workflow = WORKFLOWS_DIR / "ci.yml"
    with open(ci_workflow) as f:
        workflow = yaml.safe_load(f)

    required_jobs = ["lint", "typecheck", "test", "build"]
    for job in required_jobs:
        assert job in workflow["jobs"], f"Required job '{job}' not found in CI workflow"


def test_pr_workflow_valid_yaml() -> None:
    """Test that PR workflow is valid YAML."""
    pr_workflow = WORKFLOWS_DIR / "pr.yml"
    with open(pr_workflow) as f:
        workflow = yaml.safe_load(f)

    assert "name" in workflow
    # YAML parses 'on:' as boolean True, so check for True key
    assert True in workflow or "on" in workflow
    assert "jobs" in workflow


def test_pr_workflow_has_security_scan() -> None:
    """Test that PR workflow includes security scanning."""
    pr_workflow = WORKFLOWS_DIR / "pr.yml"
    with open(pr_workflow) as f:
        workflow = yaml.safe_load(f)

    assert "security-scan" in workflow["jobs"], "PR workflow should include security scan"


def test_workflows_use_correct_python_version() -> None:
    """Test that workflows use Python 3.11."""
    for workflow_file in WORKFLOWS_DIR.glob("*.yml"):
        with open(workflow_file) as f:
            workflow = yaml.safe_load(f)

        if "env" in workflow and "PYTHON_VERSION" in workflow["env"]:
            assert workflow["env"]["PYTHON_VERSION"] == "3.11", (
                f"Workflow {workflow_file.name} should use Python 3.11"
            )
