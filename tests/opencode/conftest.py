"""Pytest configuration for opencode integration tests."""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Generator, Dict, Any

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
def mock_env_vars() -> Dict[str, str]:
    """Mock environment variables for testing."""
    return {
        "CLICK_TEST_MODE": "1",
        "PYTHONPATH": str(Path(__file__).parent.parent.parent / "src"),
        "OPENCODE_MODEL": "glm-4.6",
    }


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, mock_env_vars):
    """Set up test environment variables."""
    for key, value in mock_env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def sample_group_file(temp_dir) -> Path:
    """Create a sample Click group file for testing."""
    content = '''
import click

@click.group()
def cli():
    """A simple CLI tool."""
    pass

@cli.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME."""
    for _ in range(count):
        click.echo(f"Hello {name}!")

@cli.command()
@click.argument("filename")
def process(filename):
    """Process a file."""
    click.echo(f"Processing {filename}")

if __name__ == "__main__":
    cli()
'''
    file_path = temp_dir / "sample_group.py"
    file_path.write_text(content.strip())
    return file_path


@pytest.fixture
def cli_runner():
    """Provide a Click CLI runner for testing."""
    from click.testing import CliRunner

    return CliRunner()


# Pytest markers
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "opencode: mark test as opencode-specific")
