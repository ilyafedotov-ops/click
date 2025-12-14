"""Tests for click argument handling and validation."""

import pytest
import tempfile
from pathlib import Path
from tests.opencode.helpers.cli_client import OpencodeTestClient
from tests.opencode.helpers.assertions import CLIAssertions
from tests.opencode.helpers.mocks import mock_stdin


class TestBasicArguments:
    """Test basic argument functionality."""

    def test_single_argument(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test single positional argument."""
        script = temp_dir / "single_arg.py"
        script.write_text("""
import click

@click.command()
@click.argument('filename')
def process(filename):
    click.echo(f'Processing file: {filename}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["test.txt"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing file: test.txt")

        result = opencode_client.run_python_script(script, [])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Missing argument")

    def test_multiple_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test multiple positional arguments."""
        script = temp_dir / "multiple_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('source')
@click.argument('destination')
@click.argument('mode')
def copy(source, destination, mode):
    click.echo(f'Copying {source} to {destination} in {mode} mode')

if __name__ == '__main__':
    copy()
""")
        result = opencode_client.run_python_script(script, ["file1.txt", "file2.txt", "backup"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Copying file1.txt to file2.txt in backup mode")

    def test_argument_type_conversion(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test argument type conversion."""
        script = temp_dir / "type_conversion.py"
        script.write_text("""
import click

@click.command()
@click.argument('count', type=int)
@click.argument('ratio', type=float)
@click.argument('flag', type=bool)
def process(count, ratio, flag):
    click.echo(f'count: {count} (type: {type(count).__name__})')
    click.echo(f'ratio: {ratio} (type: {type(ratio).__name__})')
    click.echo(f'flag: {flag} (type: {type(flag).__name__})')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["42", "3.14", "true"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "count: 42")
        CLIAssertions.assert_output_contains(result, "ratio: 3.14")
        CLIAssertions.assert_output_contains(result, "flag: True")


class TestVariadicArguments:
    """Test variadic (nargs) arguments."""

    def test_unlimited_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test unlimited number of arguments."""
        script = temp_dir / "unlimited.py"
        script.write_text("""
import click

@click.command()
@click.argument('files', nargs=-1)
def process(files):
    click.echo(f'Processing {len(files)} files:')
    for i, file in enumerate(files, 1):
        click.echo(f'  {i}. {file}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["file1.txt", "file2.txt", "file3.txt"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing 3 files:")
        CLIAssertions.assert_output_contains(result, "1. file1.txt")
        CLIAssertions.assert_output_contains(result, "2. file2.txt")
        CLIAssertions.assert_output_contains(result, "3. file3.txt")

        result = opencode_client.run_python_script(script, [])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing 0 files:")

    def test_fixed_nargs(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test fixed number of arguments."""
        script = temp_dir / "fixed_nargs.py"
        script.write_text("""
import click

@click.command()
@click.argument('coordinates', nargs=3, type=float)
def process(coordinates):
    x, y, z = coordinates
    click.echo(f'Coordinates: x={x}, y={y}, z={z}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["1.5", "2.7", "3.14"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Coordinates: x=1.5, y=2.7, z=3.14")

        result = opencode_client.run_python_script(script, ["1.5", "2.7"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Missing argument")

    def test_optional_nargs(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test optional number of arguments."""
        script = temp_dir / "optional_nargs.py"
        script.write_text("""
import click

@click.command()
@click.argument('required_arg')
@click.argument('optional_args', nargs=-1)
def process(required_arg, optional_args):
    click.echo(f'Required: {required_arg}')
    click.echo(f'Optional ({len(optional_args)}): {list(optional_args)}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["main", "opt1", "opt2"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Required: main")
        CLIAssertions.assert_output_contains(result, "Optional (2): ['opt1', 'opt2']")

        result = opencode_client.run_python_script(script, ["main"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Required: main")
        CLIAssertions.assert_output_contains(result, "Optional (0): []")


class TestArgumentValidation:
    """Test argument validation and custom validators."""

    def test_choice_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test choice argument validation."""
        script = temp_dir / "choice_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('action', type=click.Choice(['create', 'update', 'delete']))
@click.argument('format', type=click.Choice(['json', 'xml', 'yaml'], case_sensitive=False))
def process(action, format):
    click.echo(f'Action: {action}, Format: {format}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["create", "JSON"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Action: create, Format: JSON")

        result = opencode_client.run_python_script(script, ["invalid", "json"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "Invalid value")

    def test_range_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test range argument validation."""
        script = temp_dir / "range_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('port', type=click.IntRange(1, 65535))
@click.argument('percentage', type=click.IntRange(0, 100))
def configure(port, percentage):
    click.echo(f'Port: {port}, Percentage: {percentage}%')

if __name__ == '__main__':
    configure()
""")
        result = opencode_client.run_python_script(script, ["8080", "75"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Port: 8080, Percentage: 75%")

        result = opencode_client.run_python_script(script, ["70000", "75"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "70000 is not in the range")

    def test_path_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test path argument validation."""
        script = temp_dir / "path_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
def process(input_file, output_file):
    click.echo(f'Input: {input_file}')
    click.echo(f'Output: {output_file}')

if __name__ == '__main__':
    process()
""")
        # Create a test file
        test_file = temp_dir / "input.txt"
        test_file.write_text("test content")

        result = opencode_client.run_python_script(script, [str(test_file), "output.txt"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, f"Input: {test_file}")
        CLIAssertions.assert_output_contains(result, "Output: output.txt")

        result = opencode_client.run_python_script(script, ["nonexistent.txt", "output.txt"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "does not exist")

    def test_custom_validation(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test custom argument validation."""
        script = temp_dir / "custom_validation.py"
        script.write_text("""
import click
import re

def validate_email(ctx, param, value):
    if not re.match(r'^[^@]+@[^@]+\\.[^@]+$', value):
        raise click.BadParameter(f'{value} is not a valid email')
    return value

@click.command()
@click.argument('email', callback=validate_email)
@click.argument('age', type=click.IntRange(0, 120))
def register(email, age):
    click.echo(f'Email: {email}, Age: {age}')

if __name__ == '__main__':
    register()
""")
        result = opencode_client.run_python_script(script, ["test@example.com", "25"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Email: test@example.com, Age: 25")

        result = opencode_client.run_python_script(script, ["invalid-email", "25"])
        CLIAssertions.assert_failure(result)
        CLIAssertions.assert_error_contains(result, "not a valid email")


class TestArgumentHelp:
    """Test argument help generation."""

    def test_argument_help(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test argument help text."""
        script = temp_dir / "arg_help.py"
        script.write_text("""
import click

@click.command()
@click.argument('input_file', type=click.Path(exists=True), help='Input file to process')
@click.argument('output_file', help='Output file path')
@click.argument('mode', type=click.Choice(['fast', 'slow']), help='Processing mode')
def process(input_file, output_file, mode):
    click.echo('Processing...')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "input_file")
        CLIAssertions.assert_output_contains(result, "output_file")
        CLIAssertions.assert_output_contains(result, "mode")

    def test_metavar_customization(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test argument metavar customization."""
        script = temp_dir / "metavar.py"
        script.write_text("""
import click

@click.command()
@click.argument('source', metavar='SRC')
@click.argument('destination', metavar='DST')
@click.argument('files', nargs=-1, metavar='FILE...')
def copy(source, destination, files):
    click.echo('Copying...')

if __name__ == '__main__':
    copy()
""")
        result = opencode_client.run_python_script(script, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "SRC DST [FILE...]")


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_unicode_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test Unicode argument values."""
        script = temp_dir / "unicode_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('name')
@click.argument('message')
def greet(name, message):
    click.echo(f'{name} says: {message}')

if __name__ == '__main__':
    greet()
""")
        result = opencode_client.run_python_script(script, ["José", "¡Hola mundo!"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "José says: ¡Hola mundo!")

    def test_special_characters(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test special characters in arguments."""
        script = temp_dir / "special_chars.py"
        script.write_text("""
import click

@click.command()
@click.argument('pattern')
@click.argument('replacement')
def replace(pattern, replacement):
    click.echo(f'Pattern: {pattern}')
    click.echo(f'Replacement: {replacement}')

if __name__ == '__main__':
    replace()
""")
        result = opencode_client.run_python_script(script, ["[a-z]+", "[A-Z]"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Pattern: [a-z]+")
        CLIAssertions.assert_output_contains(result, "Replacement: [A-Z]")

    def test_empty_and_whitespace(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test empty and whitespace arguments."""
        script = temp_dir / "empty_whitespace.py"
        script.write_text("""
import click

@click.command()
@click.argument('text')
@click.argument('number', type=int)
def process(text, number):
    click.echo(f'Text: "{text}"')
    click.echo(f'Number: {number}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["", "0"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, 'Text: ""')
        CLIAssertions.assert_output_contains(result, "Number: 0")

    def test_large_number_of_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test handling many arguments."""
        script = temp_dir / "many_args.py"
        script.write_text("""
import click

@click.command()
@click.argument('items', nargs=-1)
def process(items):
    click.echo(f'Received {len(items)} items')
    if len(items) > 0:
        click.echo(f'First: {items[0]}')
        click.echo(f'Last: {items[-1]}')

if __name__ == '__main__':
    process()
""")
        many_args = [f"item{i}" for i in range(100)]
        result = opencode_client.run_python_script(script, many_args)
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Received 100 items")
        CLIAssertions.assert_output_contains(result, "First: item0")
        CLIAssertions.assert_output_contains(result, "Last: item99")

    def test_argument_with_options(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test mixing arguments with options."""
        script = temp_dir / "mixed_args_options.py"
        script.write_text("""
import click

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--count', '-n', default=1, type=int, help='Repeat count')
@click.argument('name')
@click.argument('message')
def communicate(verbose, count, name, message):
    for i in range(count):
        if verbose:
            click.echo(f'{i+1}/{count}: {name} says: {message}')
        else:
            click.echo(f'{name}: {message}')

if __name__ == '__main__':
    communicate()
""")
        result = opencode_client.run_python_script(script, [
            "--verbose", "--count", "2", "Alice", "Hello"
        ])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "1/2: Alice says: Hello")
        CLIAssertions.assert_output_contains(result, "2/2: Alice says: Hello")

        # Test with arguments before options (should still work)
        result = opencode_client.run_python_script(script, [
            "Bob", "Hi", "--count", "1"
        ])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Bob: Hi")


class TestComplexScenarios:
    """Test complex argument scenarios."""

    def test_nested_commands_with_arguments(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test arguments in nested command structures."""
        script = temp_dir / "nested_commands.py"
        script.write_text("""
import click

@click.group()
def cli():
    """Main command group."""
    pass

@cli.command()
@click.argument('source')
@click.argument('destination')
@click.option('--force', is_flag=True)
def copy(source, destination, force):
    """Copy files from SOURCE to DESTINATION."""
    if force:
        click.echo(f'Force copying {source} to {destination}')
    else:
        click.echo(f'Copying {source} to {destination}')

@cli.command()
@click.argument('pattern')
@click.argument('files', nargs=-1)
@click.option('--case-sensitive', is_flag=True)
def search(pattern, files, case_sensitive):
    """Search for PATTERN in FILES."""
    mode = "case-sensitive" if case_sensitive else "case-insensitive"
    click.echo(f'Searching for "{pattern}" ({mode}) in {len(files)} files')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(script, ["copy", "file1.txt", "file2.txt", "--force"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Force copying file1.txt to file2.txt")

        result = opencode_client.run_python_script(script, ["search", "hello", "file1.txt", "file2.txt"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, 'Searching for "hello" (case-insensitive) in 2 files')

    def test_argument_processing_order(self, opencode_client: OpencodeTestClient, temp_dir: Path):
        """Test argument processing and callback order."""
        script = temp_dir / "processing_order.py"
        script.write_text("""
import click

def log_callback(ctx, param, value):
    click.echo(f'Processing {param.name}: {value}')
    return value

@click.command()
@click.option('--prefix', default='PREFIX', callback=log_callback)
@click.argument('text', callback=log_callback)
@click.argument('suffix', callback=log_callback)
def process(prefix, text, suffix):
    click.echo(f'Result: {prefix}{text}{suffix}')

if __name__ == '__main__':
    process()
""")
        result = opencode_client.run_python_script(script, ["middle", "end"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing prefix: PREFIX")
        CLIAssertions.assert_output_contains(result, "Processing text: middle")
        CLIAssertions.assert_output_contains(result, "Processing suffix: end")
        CLIAssertions.assert_output_contains(result, "Result: PREFIXmiddleend")