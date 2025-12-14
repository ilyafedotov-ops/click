"""Tests for Click command groups and subcommands."""

import pytest
import tempfile
from pathlib import Path
from ..helpers.cli_client import OpencodeTestClient
from ..helpers.assertions import CLIAssertions
from ..helpers.mocks import mock_stdin, FileSystemMock


class TestCommandGroups:
    """Test command group creation and management."""

    def test_basic_group_creation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test basic command group creation."""
        group_file = temp_dir / "basic_group.py"
        group_file.write_text("""
import click

@click.group()
def cli():
    '''A simple CLI tool.'''
    pass

@cli.command()
def hello():
    '''Say hello.'''
    click.echo('Hello from group!')

@cli.command()
def goodbye():
    '''Say goodbye.'''
    click.echo('Goodbye from group!')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(group_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "A simple CLI tool")
        CLIAssertions.assert_command_in_help(result, "hello")
        CLIAssertions.assert_command_in_help(result, "goodbye")

    def test_subcommand_execution(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test subcommand execution."""
        group_file = temp_dir / "subcommands.py"
        group_file.write_text("""
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', default='World', help='Name to greet')
def hello(name):
    click.echo(f'Hello {name}!')

@cli.command()
@click.argument('message')
def echo(message):
    click.echo(message)

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(
            group_file, ["hello", "--name", "Alice"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello Alice!")

        result = opencode_client.run_python_script(group_file, ["echo", "Test message"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Test message")

    def test_nested_group_hierarchy(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test nested command group hierarchies."""
        nested_file = temp_dir / "nested_groups.py"
        nested_file.write_text("""
import click

@click.group()
def cli():
    '''Main CLI application.'''
    pass

@cli.group()
def admin():
    '''Administrative commands.'''
    pass

@admin.command()
def users():
    '''List users.'''
    click.echo('Users list')

@admin.command()
def settings():
    '''Show settings.'''
    click.echo('Admin settings')

@cli.group()
def dev():
    '''Development commands.'''
    pass

@dev.command()
def build():
    '''Build project.'''
    click.echo('Building project')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(nested_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_command_in_help(result, "admin")
        CLIAssertions.assert_command_in_help(result, "dev")

        result = opencode_client.run_python_script(nested_file, ["admin", "--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_command_in_help(result, "users")
        CLIAssertions.assert_command_in_help(result, "settings")

        result = opencode_client.run_python_script(nested_file, ["admin", "users"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Users list")

    def test_group_option_inheritance(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test group-level option inheritance."""
        inheritance_file = temp_dir / "inheritance.py"
        inheritance_file.write_text("""
import click

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose

@cli.command()
@click.pass_context
def status(ctx):
    if ctx.obj.get('verbose'):
        click.echo('Verbose: Getting detailed status...')
    click.echo('Status: OK')

@cli.command()
@click.pass_context
def info(ctx):
    if ctx.obj.get('verbose'):
        click.echo('Verbose: Getting detailed info...')
    click.echo('Info: Application v1.0')

if __name__ == '__main__':
    cli(obj={})
""")
        result = opencode_client.run_python_script(inheritance_file, ["status"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Status: OK")
        CLIAssertions.assert_output_not_contains(result, "Verbose:")

        result = opencode_client.run_python_script(
            inheritance_file, ["--verbose", "status"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(
            result, "Verbose: Getting detailed status..."
        )
        CLIAssertions.assert_output_contains(result, "Status: OK")

    def test_dynamic_group_registration(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test dynamic command group registration."""
        dynamic_file = temp_dir / "dynamic.py"
        dynamic_file.write_text("""
import click

@click.group()
def cli():
    pass

def register_plugin_commands(group):
    @group.command()
    def plugin1():
        click.echo('Plugin 1 command')
    
    @group.command()
    @click.option('--flag', is_flag=True)
    def plugin2(flag):
        if flag:
            click.echo('Plugin 2 with flag')
        else:
            click.echo('Plugin 2 without flag')
    
    return group

cli = register_plugin_commands(cli)

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(dynamic_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_command_in_help(result, "plugin1")
        CLIAssertions.assert_command_in_help(result, "plugin2")

        result = opencode_client.run_python_script(dynamic_file, ["plugin1"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Plugin 1 command")

        result = opencode_client.run_python_script(dynamic_file, ["plugin2", "--flag"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Plugin 2 with flag")

    def test_group_help_text_generation(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test group help text and documentation generation."""
        help_file = temp_dir / "help_text.py"
        help_file.write_text("""
import click

@click.group(help='''A comprehensive CLI tool for managing applications.

This tool provides various commands for deployment, monitoring,
and configuration management.
''')
@click.version_option(version='1.0.0')
def cli():
    '''Main application CLI.'''
    pass

@cli.command()
@click.option('--format', type=click.Choice(['json', 'yaml', 'table']), 
              default='table', help='Output format')
def status(format):
    '''Show application status.
    
    Displays current application status including health checks,
    resource usage, and active connections.
    '''
    click.echo(f'Status in {format} format')

@cli.command()
@click.argument('env', type=click.Choice(['dev', 'staging', 'prod']))
def deploy(env):
    '''Deploy application to specified environment.
    
    ENV: Target environment for deployment.
    '''
    click.echo(f'Deploying to {env}')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(help_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "A comprehensive CLI tool")
        CLIAssertions.assert_output_contains(result, "deployment, monitoring")
        CLIAssertions.assert_output_contains(result, "--version")

        result = opencode_client.run_python_script(help_file, ["status", "--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Show application status")
        CLIAssertions.assert_output_contains(result, "health checks")
        CLIAssertions.assert_option_in_help(result, "--format")

        result = opencode_client.run_python_script(help_file, ["deploy", "--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(
            result, "Deploy application to specified environment"
        )
        CLIAssertions.assert_output_contains(result, "ENV: Target environment")

    def test_group_command_discovery(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test command discovery and validation within groups."""
        discovery_file = temp_dir / "discovery.py"
        discovery_file.write_text("""
import click

@click.group()
def cli():
    pass

@cli.command()
def cmd1():
    '''First command.'''
    click.echo('Command 1')

@cli.command()
def cmd2():
    '''Second command.'''
    click.echo('Command 2')

@cli.command(hidden=True)
def hidden_cmd():
    '''Hidden command.'''
    click.echo('Hidden')

if __name__ == '__main__':
    cli()
""")
        result = opencode_client.run_python_script(discovery_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_command_in_help(result, "cmd1")
        CLIAssertions.assert_command_in_help(result, "cmd2")
        CLIAssertions.assert_output_not_contains(result, "hidden_cmd")

        result = opencode_client.run_python_script(discovery_file, ["cmd1"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Command 1")

        result = opencode_client.run_python_script(discovery_file, ["hidden_cmd"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hidden")

        result = opencode_client.run_python_script(discovery_file, ["nonexistent"])
        CLIAssertions.assert_failure(result)

    def test_group_context_passing(
        self, opencode_client: OpencodeTestClient, temp_dir: Path
    ):
        """Test context passing between group and commands."""
        context_file = temp_dir / "context.py"
        context_file.write_text("""
import click

@click.group()
@click.option('--config', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, config):
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['initialized'] = True

@cli.command()
@click.pass_context
def show_config(ctx):
    if ctx.obj.get('config'):
        click.echo(f'Config file: {ctx.obj["config"]}')
    else:
        click.echo('No config file specified')
    click.echo(f'Initialized: {ctx.obj.get("initialized", False)}')

@cli.command()
@click.option('--debug', is_flag=True)
@click.pass_context
def process(ctx, debug):
    click.echo(f'Processing with debug={debug}')
    click.echo(f'Config available: {ctx.obj.get("config") is not None}')

if __name__ == '__main__':
    cli(obj={})
""")
        result = opencode_client.run_python_script(context_file, ["show-config"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "No config file specified")
        CLIAssertions.assert_output_contains(result, "Initialized: True")

        result = opencode_client.run_python_script(context_file, ["process", "--debug"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Processing with debug=True")
        CLIAssertions.assert_output_contains(result, "Config available: False")
