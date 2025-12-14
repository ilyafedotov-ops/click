"""Tests for advanced Click features and scenarios."""

import pytest
import tempfile
import json
from pathlib import Path
from tests.opencode.helpers.cli_client import OpencodeTestClient
from tests.opencode.helpers.assertions import CLIAssertions
from tests.opencode.helpers.mocks import mock_stdin, FileSystemMock


class TestAdvancedFeatures:
    """Test advanced Click features and edge cases."""

    def test_command_chaining(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test command chaining and pipeline operations."""
        chaining_file = temp_dir / "chaining.py"
        chaining_file.write_text("""
import click

@click.group(chain=True)
def cli():
    '''Command chaining enabled CLI.'''
    pass

@cli.command()
@click.option('--message', default='Hello', help='Message to display')
def step1(message):
    '''First step in chain.'''
    click.echo(f'Step 1: {message}')

@cli.command()
@click.option('--count', default=1, help='Number of repetitions')
def step2(count):
    '''Second step in chain.'''
    for i in range(count):
        click.echo(f'Step 2: Repetition {i+1}')

@cli.command()
def step3():
    '''Final step in chain.'''
    click.echo('Step 3: Complete')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(
            chaining_file,
            ["step1", "--message", "Test", "step2", "--count", "2", "step3"],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Step 1: Test")
        CLIAssertions.assert_output_contains(result, "Step 2: Repetition 1")
        CLIAssertions.assert_output_contains(result, "Step 2: Repetition 2")
        CLIAssertions.assert_output_contains(result, "Step 3: Complete")

    def test_context_passing_between_commands(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test context passing between commands."""
        context_file = temp_dir / "context_passing.py"
        context_file.write_text("""
import click

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['shared_data'] = []

@cli.command()
@click.argument('value')
@click.pass_context
def add(ctx, value):
    '''Add value to shared data.'''
    ctx.obj['shared_data'].append(value)
    click.echo(f'Added: {value}')

@cli.command()
@click.pass_context
def show(ctx):
    '''Show shared data.'''
    data = ctx.obj['shared_data']
    if data:
        click.echo(f'Shared data: {", ".join(data)}')
    else:
        click.echo('No data')

@cli.command()
@click.pass_context
def clear(ctx):
    '''Clear shared data.'''
    ctx.obj['shared_data'].clear()
    click.echo('Data cleared')

if __name__ == '__main__':
    cli(obj={})
""")
        result = opencode_client.run_python_script(context_file, ["show"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "No data")

        result = opencode_client.run_python_script(context_file, ["add", "first"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Added: first")

        result = opencode_client.run_python_script(context_file, ["add", "second"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Added: second")

        result = opencode_client.run_python_script(context_file, ["show"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Shared data: first, second")

    def test_callback_function_execution(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test callback function execution and error handling."""
        callback_file = temp_dir / "callbacks.py"
        callback_file.write_text("""
import click

def validate_input(ctx, param, value):
    if len(value) < 3:
        raise click.BadParameter('Value must be at least 3 characters')
    return value.upper()

def process_result(ctx, param, value):
    click.echo(f'Processing result: {value}')
    return value * 2

@click.command()
@click.option('--name', callback=validate_input, help='Name (min 3 chars)')
@click.option('--multiplier', type=int, callback=process_result, help='Multiplier')
@click.pass_context
def process(ctx, name, multiplier):
    '''Process data with callbacks.'''
    click.echo(f'Processing {name} with multiplier {multiplier}')

@click.command()
@click.option('--file', type=click.File('r'), help='Input file')
def read_file(file):
    '''Read file with error handling.'''
    try:
        content = file.read()
        click.echo(f'File content ({len(content)} chars): {content[:50]}...')
    except Exception as e:
        click.echo(f'Error reading file: {e}', err=True)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        process()
    else:
        read_file()
""")
        result = opencode_client.run_python_script(
            callback_file, ["process", "--name", "test", "--multiplier", "5"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing result: 5")
        CLIAssertions.assert_output_contains(
            result, "Processing TEST with multiplier 10"
        )

        result = opencode_client.run_python_script(
            callback_file, ["process", "--name", "ab"]
        )
        CLIAssertions.assert_failure(result)

    def test_custom_parameter_types(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test custom parameter type validation."""
        custom_types_file = temp_dir / "custom_types.py"
        custom_types_file.write_text("""
import click
import re

class EmailType(click.ParamType):
    name = 'email'
    
    def convert(self, value, param, ctx):
        if not re.match(r'^[^@]+@[^@]+\\.[^@]+$', value):
            self.fail(f'{value!r} is not a valid email address', param, ctx)
        return value.lower()

class RangeType(click.ParamType):
    name = 'range'
    
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
    
    def convert(self, value, param, ctx):
        try:
            num_val = int(value)
        except ValueError:
            self.fail(f'{value!r} is not a valid integer', param, ctx)
        
        if not (self.min_val <= num_val <= self.max_val):
            self.fail(f'{num_val} is not in range {self.min_val}-{self.max_val}', param, ctx)
        return num_val

@click.command()
@click.option('--email', type=EmailType(), help='Email address')
@click.option('--age', type=RangeType(0, 120), help='Age (0-120)')
@click.option('--score', type=click.FloatRange(0.0, 100.0), help='Score (0-100)')
def validate(email, age, score):
    '''Validate custom parameter types.'''
    click.echo(f'Email: {email}')
    click.echo(f'Age: {age}')
    click.echo(f'Score: {score}')

if __name__ == '__main__':
    validate()
""")
        result = opencode_client.run_python_script(
            custom_types_file,
            ["--email", "TEST@EXAMPLE.COM", "--age", "25", "--score", "85.5"],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Email: test@example.com")
        CLIAssertions.assert_output_contains(result, "Age: 25")
        CLIAssertions.assert_output_contains(result, "Score: 85.5")

        result = opencode_client.run_python_script(
            custom_types_file, ["--email", "invalid-email"]
        )
        CLIAssertions.assert_failure(result)

        result = opencode_client.run_python_script(custom_types_file, ["--age", "150"])
        CLIAssertions.assert_failure(result)

    def test_command_aliases_and_shortcuts(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test command aliases and shortcuts."""
        aliases_file = temp_dir / "aliases.py"
        aliases_file.write_text("""
import click

@click.group()
def cli():
    '''CLI with command aliases.'''
    pass

@cli.command('list')
@cli.command('ls')
@cli.command('l')
def list_items():
    '''List items (alias: ls, l).'''
    click.echo('Listing items...')

@cli.command()
@click.option('--all', 'show_all', is_flag=True, help='Show all')
def remove(show_all):
    '''Remove items.'''
    if show_all:
        click.echo('Removing all items...')
    else:
        click.echo('Removing selected items...')

@cli.command('create')
@cli.command('new')
@cli.command('add')
@click.argument('name')
def create_item(name):
    '''Create new item (alias: new, add).'''
    click.echo(f'Creating item: {name}')

if __name__ == '__main__':
    cli()
""")
        for cmd in ["list", "ls", "l"]:
            result = opencode_client.run_python_script(aliases_file, [cmd])
            CLIAssertions.assert_success(result)
            CLIAssertions.assert_output_contains(result, "Listing items...")

        for cmd in ["create", "new", "add"]:
            result = opencode_client.run_python_script(aliases_file, [cmd, "test"])
            CLIAssertions.assert_success(result)
            CLIAssertions.assert_output_contains(result, "Creating item: test")

        result = opencode_client.run_python_script(aliases_file, ["remove", "--all"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Removing all items...")

    def test_conditional_command_execution(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test conditional command execution."""
        conditional_file = temp_dir / "conditional.py"
        conditional_file.write_text("""
import click
import os

@click.group()
@click.option('--env', type=click.Choice(['dev', 'staging', 'prod']), 
              default='dev', help='Environment')
@click.pass_context
def cli(ctx, env):
    ctx.ensure_object(dict)
    ctx.obj['env'] = env

@cli.command()
@click.option('--force', is_flag=True, help='Force execution')
@click.pass_context
def deploy(ctx, force):
    '''Deploy to environment.'''
    env = ctx.obj['env']
    
    if env == 'prod' and not force:
        click.echo('Cannot deploy to production without --force flag')
        ctx.exit(1)
    
    click.echo(f'Deploying to {env} environment...')

@cli.command()
@click.pass_context
def status(ctx):
    '''Show environment status.'''
    env = ctx.obj['env']
    
    if env == 'dev':
        click.echo('Development environment - all features enabled')
    elif env == 'staging':
        click.echo('Staging environment - testing features')
    elif env == 'prod':
        click.echo('Production environment - stable features only')

@cli.command()
@click.pass_context
def debug(ctx):
    '''Debug command (dev only).'''
    env = ctx.obj['env']
    
    if env != 'dev':
        click.echo('Debug command only available in development environment')
        ctx.exit(1)
    
    click.echo('Debug mode activated')

if __name__ == '__main__':
    cli(obj={})
""")
        result = opencode_client.run_python_script(
            conditional_file, ["--env", "dev", "status"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Development environment")

        result = opencode_client.run_python_script(
            conditional_file, ["--env", "prod", "deploy"]
        )
        CLIAssertions.assert_failure(result)

        result = opencode_client.run_python_script(
            conditional_file, ["--env", "prod", "deploy", "--force"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Deploying to prod environment")

        result = opencode_client.run_python_script(
            conditional_file, ["--env", "staging", "debug"]
        )
        CLIAssertions.assert_failure(result)

    def test_error_handling_and_recovery(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test error handling and graceful degradation."""
        error_handling_file = temp_dir / "error_handling.py"
        error_handling_file.write_text("""
import click
import sys

class CustomError(click.ClickException):
    def __init__(self, message, recoverable=False):
        super().__init__(message)
        self.recoverable = recoverable
    
    def show(self, file=None):
        if self.recoverable:
            click.echo(f'Recoverable error: {self.message}', err=True)
        else:
            click.echo(f'Fatal error: {self.message}', err=True)

@click.command()
@click.option('--file', type=click.Path(exists=True), help='Input file')
@click.option('--recover', is_flag=True, help='Enable recovery mode')
def process_file(file, recover):
    '''Process file with error handling.'''
    try:
        if not file:
            if recover:
                click.echo('No file specified, using default input')
                return
            else:
                raise CustomError('No file specified', recoverable=False)
        
        click.echo(f'Processing file: {file}')
        
    except CustomError as e:
        e.show()
        if not e.recoverable:
            sys.exit(1)
    except Exception as e:
        click.echo(f'Unexpected error: {e}', err=True)
        if recover:
            click.echo('Attempting recovery...')
        else:
            sys.exit(1)

@click.command()
@click.option('--risky', is_flag=True, help='Enable risky operation')
def risky_operation(risky):
    '''Perform risky operation with validation.'''
    if risky:
        click.echo('Performing risky operation...')
        if click.confirm('This is dangerous. Continue?'):
            click.echo('Operation completed successfully')
        else:
            click.echo('Operation cancelled')
    else:
        click.echo('Safe operation completed')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'risky':
        risky_operation()
    else:
        process_file()
""")
        result = opencode_client.run_python_script(error_handling_file, ["--recover"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(
            result, "No file specified, using default input"
        )

        result = opencode_client.run_python_script(error_handling_file, [])
        CLIAssertions.assert_failure(result)

        with mock_stdin(["n"]):
            result = opencode_client.run_python_script(
                error_handling_file, ["risky", "--risky"]
            )
            CLIAssertions.assert_success(result)
            CLIAssertions.assert_output_contains(result, "Operation cancelled")

    def test_multi_value_parameters(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test multi-value parameters and collections."""
        multi_value_file = temp_dir / "multi_value.py"
        multi_value_file.write_text("""
import click

@click.command()
@click.option('--tags', multiple=True, help='Tags to add')
@click.option('--numbers', type=int, multiple=True, help='Numbers to process')
@click.argument('files', nargs=-1, type=click.Path())
def process(tags, numbers, files):
    '''Process multiple values.'''
    click.echo(f'Tags: {list(tags)}')
    click.echo(f'Numbers: {list(numbers)}')
    click.echo(f'Files: {list(files)}')
    
    if tags:
        click.echo(f'Processing {len(tags)} tags')
    if numbers:
        total = sum(numbers)
        click.echo(f'Sum of numbers: {total}')
    if files:
        click.echo(f'Processing {len(files)} files')

@click.command()
@click.option('--config', type=(str, str), multiple=True, 
              help='Key-value pairs (key=value)')
def configure(config):
    '''Configure with key-value pairs.'''
    click.echo('Configuration:')
    for key, value in config:
        click.echo(f'  {key}: {value}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'configure':
        configure()
    else:
        process()
""")
        result = opencode_client.run_python_script(
            multi_value_file,
            [
                "--tags",
                "tag1",
                "--tags",
                "tag2",
                "--numbers",
                "1",
                "--numbers",
                "2",
                "--numbers",
                "3",
                "file1.txt",
                "file2.txt",
            ],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Tags: ['tag1', 'tag2']")
        CLIAssertions.assert_output_contains(result, "Numbers: [1, 2, 3]")
        CLIAssertions.assert_output_contains(
            result, "Files: ['file1.txt', 'file2.txt']"
        )
        CLIAssertions.assert_output_contains(result, "Sum of numbers: 6")

        result = opencode_client.run_python_script(
            multi_value_file,
            ["configure", "--config", "host=localhost", "--config", "port=8080"],
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "host: localhost")
        CLIAssertions.assert_output_contains(result, "port: 8080")
