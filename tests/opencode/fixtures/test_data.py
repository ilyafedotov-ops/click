"""Additional test data fixtures for opencode click testing."""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any, List


@pytest.fixture
def sample_text_file(temp_dir: Path) -> Path:
    """Create a sample text file for testing."""
    text_file = temp_dir / "sample.txt"
    text_file.write_text("""Hello World
This is a test file
With multiple lines
Containing various content
For testing purposes
""")
    return text_file


@pytest.fixture
def sample_json_file(temp_dir: Path) -> Path:
    """Create a sample JSON file for testing."""
    json_file = temp_dir / "data.json"
    data = {
        "users": [
            {"name": "Alice", "age": 30, "city": "New York"},
            {"name": "Bob", "age": 25, "city": "San Francisco"},
        ],
        "settings": {
            "debug": True,
            "timeout": 30,
        },
    }
    json_file.write_text(json.dumps(data, indent=2))
    return json_file


@pytest.fixture
def sample_csv_file(temp_dir: Path) -> Path:
    """Create a sample CSV file for testing."""
    csv_file = temp_dir / "data.csv"
    csv_content = """name,age,city
Alice,30,New York
Bob,25,San Francisco
Charlie,35,Chicago
"""
    csv_file.write_text(csv_content)
    return csv_file


@pytest.fixture
def complex_command_file(temp_dir: Path) -> Path:
    """Create a complex command file for testing."""
    command_file = temp_dir / "complex_cli.py"
    command_file.write_text("""import click
import sys

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    '''A complex CLI application for testing.'''
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.command()
@click.argument('name')
@click.option('--count', '-c', default=1, help='Number of times to greet')
@click.pass_context
def greet(ctx, name, count):
    '''Greet someone multiple times.'''
    for i in range(count):
        if ctx.obj.get('verbose'):
            click.echo(f'[{i+1}/{count}] Greeting {name}')
        else:
            click.echo(f'Hello {name}!')

@cli.group()
def admin():
    '''Administrative commands.'''
    pass

@admin.command()
@click.argument('username')
@click.option('--role', default='user', help='User role')
def create_user(username, role):
    '''Create a new user.'''
    click.echo(f'Created user: {username} with role: {role}')

@admin.command()
@click.option('--format', type=click.Choice(['json', 'text']), default='text')
def show_config(format):
    '''Show configuration.'''
    config = {'debug': True, 'version': '1.0.0'}
    if format == 'json':
        import json
        click.echo(json.dumps(config, indent=2))
    else:
        for key, value in config.items():
            click.echo(f'{key}: {value}')

if __name__ == '__main__':
    cli()
""")
    return command_file


@pytest.fixture
def error_command_file(temp_dir: Path) -> Path:
    """Create a command file that produces errors for testing."""
    command_file = temp_dir / "error_cli.py"
    command_file.write_text("""import click

@click.command()
@click.option('--fail', is_flag=True, help='Force failure')
def error_test(fail):
    '''A command that can fail for testing error handling.'''
    if fail:
        raise click.ClickException('This is a test error')
    click.echo('Success!')

@click.command()
@click.argument('filename')
@click.option('--strict', is_flag=True, help='Strict file checking')
def file_test(filename, strict):
    '''Test file operations with error handling.'''
    try:
        with open(filename, 'r') as f:
            content = f.read()
        if strict and not content.strip():
            raise click.ClickException('File is empty')
        click.echo(f'File {filename} has {len(content)} characters')
    except FileNotFoundError:
        raise click.ClickException(f'File not found: {filename}')

if __name__ == '__main__':
    error_test()
""")
    return command_file


@pytest.fixture
def mock_opencode_config() -> Dict[str, Any]:
    """Mock opencode configuration for testing."""
    return {
        "model": "glm-4.6",
        "timeout": 30,
        "max_tokens": 4096,
        "temperature": 0.7,
        "tools": ["bash", "read", "write", "edit"],
        "work_dir": "/tmp/opencode_test",
    }


@pytest.fixture
def mock_glm46_response() -> Dict[str, Any]:
    """Mock GLM-4.6 response for testing."""
    return {
        "id": "test-response-123",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "glm-4.6",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "This is a mock response from GLM-4.6 for testing purposes.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 15,
            "total_tokens": 25,
        },
    }


@pytest.fixture
def sample_test_data() -> Dict[str, List[Dict[str, Any]]]:
    """Sample test data for parametrized tests."""
    return {
        "commands": [
            {"name": "hello", "args": ["--name", "World"], "expected": "Hello World!"},
            {"name": "count", "args": ["--number", "5"], "expected": "5"},
            {
                "name": "process",
                "args": ["--input", "test.txt"],
                "expected": "Processing test.txt",
            },
        ],
        "options": [
            {"option": "--verbose", "type": "flag", "default": False},
            {"option": "--count", "type": "int", "default": 1},
            {"option": "--name", "type": "str", "required": True},
        ],
        "errors": [
            {"input": "invalid", "error_type": "ValueError"},
            {"input": "", "error_type": "ValidationError"},
            {"input": None, "error_type": "MissingParameter"},
        ],
    }
