"""Pytest configuration for opencode click tests."""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Generator, Any

from .helpers.cli_client import OpencodeTestClient


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def opencode_client() -> OpencodeTestClient:
    """Create an OpencodeTestClient instance for CLI testing."""
    return OpencodeTestClient()


@pytest.fixture
def sample_command_file(temp_dir: Path) -> Path:
    """Create a sample command file for testing."""
    command_file = temp_dir / "sample_command.py"
    command_file.write_text("""
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    '''Simple program that greets NAME for a total of COUNT times.'''
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
""")
    return command_file


@pytest.fixture
def mock_env_vars() -> dict[str, str]:
    """Mock environment variables for testing."""
    return {
        "CLICK_TESTING": "true",
        "PYTHONPATH": str(Path(__file__).parent.parent.parent / "src"),
    }


@pytest.fixture(autouse=True)
def setup_test_env(
    monkeypatch: pytest.MonkeyPatch, mock_env_vars: dict[str, str]
) -> None:
    """Set up test environment variables."""
    for key, value in mock_env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def capture_output() -> Generator[tuple[list[str], list[str]], None, None]:
    """Capture stdout and stderr during test execution."""
    import sys
    from io import StringIO

    stdout_capture = StringIO()
    stderr_capture = StringIO()

    old_stdout = sys.stdout
    old_stderr = sys.stderr

    try:
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        yield ([], [])
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr


@pytest.fixture
def cli_runner():
    """Provide a Click CLI runner for testing."""
    from click.testing import CliRunner

    return CliRunner()


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Get the test data directory."""
    return Path(__file__).parent / "fixtures"
