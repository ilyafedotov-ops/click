"""Tests for click option parsing and validation."""

import pytest
import tempfile
from pathlib import Path
from tests.opencode.helpers.cli_client import OpencodeTestClient
from tests.opencode.helpers.assertions import CLIAssertions
from tests.opencode.helpers.mocks import mock_stdin


class TestBasicOptions:
    """Test basic option functionality."""

    def test_required_option(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test required option validation."""
        script = temp_dir / "required_option.py"
        script.write_text("""
import click

@click.command()
@click.option('--name', required=True, help='Name is required')
@click.option('--age', type=int, help='Optional age')
def greet(name, age):
    click.echo(f'Hello {name}!')
    if age:
        click.echo(f'Age: {age}')

if __name__ == '__main__':
    greet()
""")
        result = opencode_client.run_python_script(script, ["--name", "Alice"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello Alice!")

        result = opencode_client.run_python_script(script, [])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Missing option")

    def test_option_type_conversion(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test option type conversion."""
        script = temp_dir / "type_conversion.py"
        script.write_text("""
import click

@click.command()
@click.option('--count', type=int, default=1)
@click.option('--ratio', type=float, default=0.5)
@click.option('--verbose', is_flag=True)
@click.option('--choice', type=click.Choice(['a', 'b', 'c']))
def process(count, ratio, verbose, choice):
    click.echo(f'count: {count} (type: {type(count).__name__})')
    click.echo(f'ratio: {ratio} (type: {type(ratio).__name__})')
    click.echo(f'verbose: {verbose} (type: {type(verbose).__name__})')
    if choice:
        click.echo(f'choice: {choice} (type: {type(choice).__name__})')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(
            script, ["--count", "42", "--ratio", "3.14", "--verbose", "--choice", "b"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "count: 42")
        CLIAssertions.assert_output_contains(result, "ratio: 3.14")
        CLIAssertions.assert_output_contains(result, "verbose: True")
        CLIAssertions.assert_output_contains(result, "choice: b")

    def test_option_defaults(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test option default values."""
        script = temp_dir / "defaults.py"
        script.write_text("""
import click

@click.command()
@click.option('--name', default='World', help='Name to greet')
@click.option('--count', default=1, type=int)
@click.option('--verbose', is_flag=True, default=False)
def greet(name, count, verbose):
    for i in range(count):
        if verbose:
            click.echo(f'Greeting {i+1}: Hello {name}!')
        else:
            click.echo(f'Hello {name}!')

if __name__ == '__main__':
    greet()
""")
        result = opencode_client.run_python_script(script, [])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello World!")

        result = opencode_client.run_python_script(
            script, ["--name", "Alice", "--count", "2"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_line_count(result, 2)


class TestAdvancedOptions:
    """Test advanced option features."""

    def test_multiple_options(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test multiple value options."""
        script = temp_dir / "multiple.py"
        script.write_text("""
import click

@click.command()
@click.option('--file', multiple=True, help='Files to process')
@click.option('--tag', multiple=True, help='Tags to add')
def process(file, tag):
    click.echo(f'Files: {list(file)}')
    click.echo(f'Tags: {list(tag)}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(
            script,
            ["--file", "a.txt", "--file", "b.txt", "--tag", "test", "--tag", "prod"],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Files: ['a.txt', 'b.txt']")
        CLIAssertions.assert_output_contains(result, "Tags: ['test', 'prod']")

    def test_counting_options(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test counting flags."""
        script = temp_dir / "counting.py"
        script.write_text("""
import click

@click.command()
@click.option('-v', '--verbose', count=True, help='Increase verbosity')
@click.option('-q', '--quiet', count=True, help='Decrease verbosity')
def process(verbose, quiet):
    level = verbose - quiet
    click.echo(f'Verbosity level: {level}')
    click.echo(f'Verbose count: {verbose}')
    click.echo(f'Quiet count: {quiet}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["-vvv", "-q"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Verbosity level: 2")
        CLIAssertions.assert_output_contains(result, "Verbose count: 3")
        CLIAssertions.assert_output_contains(result, "Quiet count: 1")

    def test_option_callbacks(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test option validation callbacks."""
        script = temp_dir / "callbacks.py"
        script.write_text("""
import click

def validate_range(ctx, param, value):
    if value < 0 or value > 100:
        raise click.BadParameter('Value must be between 0 and 100')
    return value

@click.command()
@click.option('--percentage', type=int, callback=validate_range, help='Percentage (0-100)')
def process(percentage):
    click.echo(f'Valid percentage: {percentage}%')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["--percentage", "75"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Valid percentage: 75%")

        result = opencode_client.run_python_script(script, ["--percentage", "150"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Value must be between 0 and 100")

    def test_environment_variables(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test environment variable integration."""
        script = temp_dir / "env_vars.py"
        script.write_text("""
import click
import os

@click.command()
@click.option('--api-key', envvar='API_KEY', help='API key')
@click.option('--debug', envvar='DEBUG', is_flag=True, help='Debug mode')
def process(api_key, debug):
    click.echo(f'API Key: {api_key or "Not set"}')
    click.echo(f'Debug: {debug}')

if __name__ == '__main__':
    process()
""")
        env = {"API_KEY": "secret123", "DEBUG": "1"}
        result = opencode_client.run_python_script(script, [], env=env)
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "API Key: secret123")
        CLIAssertions.assert_output_contains(result, "Debug: True")


class TestOptionValidation:
    """Test option validation and error handling."""

    def test_choice_validation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test choice option validation."""
        script = temp_dir / "choice_validation.py"
        script.write_text("""
import click

@click.command()
@click.option('--color', type=click.Choice(['red', 'green', 'blue']))
@click.option('--size', type=click.Choice(['S', 'M', 'L'], case_sensitive=False))
def configure(color, size):
    click.echo(f'Color: {color}')
    click.echo(f'Size: {size}')

if __name__ == '__main__':
    configure()
""")
        result = opencode_client.run_python_script(
            script, ["--color", "red", "--size", "m"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Color: red")
        CLIAssertions.assert_output_contains(result, "Size: M")

        result = opencode_client.run_python_script(script, ["--color", "yellow"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Invalid value")

    def test_custom_validation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test custom validation functions."""
        script = temp_dir / "custom_validation.py"
        script.write_text("""
import click
import re

def validate_email(ctx, param, value):
    if not re.match(r'^[^@]+@[^@]+\\.[^@]+$', value):
        raise click.BadParameter(f'{value} is not a valid email')
    return value

@click.command()
@click.option('--email', callback=validate_email, required=True)
@click.option('--age', type=click.IntRange(0, 120))
def register(email, age):
    click.echo(f'Email: {email}')
    if age is not None:
        click.echo(f'Age: {age}')

if __name__ == '__main__':
    register()
""")
        result = opencode_client.run_python_script(
            script, ["--email", "test@example.com", "--age", "25"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Email: test@example.com")

        result = opencode_client.run_python_script(script, ["--email", "invalid-email"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "not a valid email")

    def test_range_validation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test range validation."""
        script = temp_dir / "range_validation.py"
        script.write_text("""
import click

@click.command()
@click.option('--port', type=click.IntRange(1, 65535))
@click.option('--ratio', type=click.FloatRange(0.0, 1.0))
@click.option('--count', type=click.IntRange(0))
def configure(port, ratio, count):
    click.echo(f'Port: {port}')
    click.echo(f'Ratio: {ratio}')
    click.echo(f'Count: {count}')

if __name__ == '__main__':
    configure()
""")
        result = opencode_client.run_python_script(
            script, ["--port", "8080", "--ratio", "0.5", "--count", "5"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Port: 8080")
        CLIAssertions.assert_output_contains(result, "Ratio: 0.5")
        CLIAssertions.assert_output_contains(result, "Count: 5")

        result = opencode_client.run_python_script(script, ["--port", "70000"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "70000 is not in the range")


class TestOptionHelp:
    """Test option help generation."""

    def test_help_text_generation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test help text for various option types."""
        script = temp_dir / "help_text.py"
        script.write_text("""
import click

@click.command()
@click.option('--simple', help='A simple option')
@click.option('--with-default', default='default_value', help='Option with default')
@click.option('--required', required=True, help='Required option')
@click.option('--choice', type=click.Choice(['a', 'b']), help='Choice option')
@click.option('--flag', is_flag=True, help='Boolean flag')
@click.option('--count', count=True, help='Counting flag')
@click.option('--hidden', hidden=True, help='Hidden option')
def cli(simple, with_default, required, choice, flag, count, hidden):
    click.echo('Command executed')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(script, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "--simple")
        CLIAssertions.assert_output_contains(result, "--with-default")
        CLIAssertions.assert_output_contains(result, "--required")
        CLIAssertions.assert_output_contains(result, "--choice")
        CLIAssertions.assert_output_contains(result, "--flag")
        CLIAssertions.assert_output_contains(result, "--count")
        CLIAssertions.assert_output_not_contains(result, "--hidden")

    def test_option_metavar(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test option metavar customization."""
        script = temp_dir / "metavar.py"
        script.write_text("""
import click

@click.command()
@click.option('--file', metavar='PATH', help='Input file')
@click.option('--number', metavar='N', type=int, help='A number')
@click.option('--range', metavar='START-END', help='Range specification')
def process(file, number, range):
    click.echo('Processing...')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "--file PATH")
        CLIAssertions.assert_output_contains(result, "--number N")
        CLIAssertions.assert_output_contains(result, "--range START-END")


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_unicode_options(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test Unicode option values."""
        script = temp_dir / "unicode.py"
        script.write_text("""
import click

@click.command()
@click.option('--name', help='Name with Unicode support')
@click.option('--emoji', help='Emoji option')
def greet(name, emoji):
    click.echo(f'Hello {name}! {emoji}')

if __name__ == '__main__':
    greet()
""")
        result = opencode_client.run_python_script(
            script, ["--name", "José", "--emoji", "👋"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello José! 👋")

    def test_special_characters(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test special characters in option values."""
        script = temp_dir / "special_chars.py"
        script.write_text("""
import click

@click.command()
@click.option('--text', help='Text with special characters')
@click.option('--json', help='JSON-like string')
def process(text, json):
    click.echo(f'Text: {text}')
    click.echo(f'JSON: {json}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(
            script,
            [
                "--text",
                "Hello & <world>!",
                "--json",
                '{"key": "value", "array": [1, 2, 3]}',
            ],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Text: Hello & <world>!")
        CLIAssertions.assert_output_contains(
            result, 'JSON: {"key": "value", "array": [1, 2, 3]}'
        )

    def test_empty_and_none_values(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test empty and None option values."""
        script = temp_dir / "empty_none.py"
        script.write_text("""
import click

@click.command()
@click.option('--empty-string', default='', help='Empty string default')
@click.option('--none-value', default=None, help='None default')
@click.option('--flag', is_flag=True, default=None, help='Flag with None default')
def process(empty_string, none_value, flag):
    click.echo(f'Empty string: "{empty_string}"')
    click.echo(f'None value: {none_value}')
    click.echo(f'Flag: {flag}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, [])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, 'Empty string: ""')
        CLIAssertions.assert_output_contains(result, "None value: None")
        CLIAssertions.assert_output_contains(result, "Flag: None")
