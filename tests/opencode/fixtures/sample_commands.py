"""Sample commands for testing opencode click integration."""

import click
import sys
from typing import Optional


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def hello(count: int, name: str, verbose: bool) -> None:
    """Simple program that greets NAME for a total of COUNT times."""
    if verbose:
        click.echo(f"Starting greeting process for {name}")

    for i in range(count):
        click.echo(f"Hello {name}!")
        if verbose:
            click.echo(f"  Greeting {i + 1} of {count}")

    if verbose:
        click.echo("Greeting process completed")


@click.group()
def cli() -> None:
    """A sample CLI application for testing."""
    pass


@cli.command()
@click.argument("filename")
@click.option("--lines", "-n", default=10, help="Number of lines to display")
def head(filename: str, lines: int) -> None:
    """Display first lines of a file."""
    try:
        with open(filename, "r") as f:
            for i, line in enumerate(f):
                if i >= lines:
                    break
                click.echo(line.rstrip())
    except FileNotFoundError:
        click.echo(f"Error: File '{filename}' not found", err=True)
        sys.exit(1)


@cli.command()
@click.option("--pattern", "-p", required=True, help="Search pattern")
@click.option(
    "--case-sensitive", is_flag=True, default=False, help="Case sensitive search"
)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
def grep(pattern: str, case_sensitive: bool, files: tuple[str, ...]) -> None:
    """Search for pattern in files."""
    if not files:
        click.echo("Error: No files specified", err=True)
        sys.exit(1)

    search_pattern = pattern if case_sensitive else pattern.lower()

    for file_path in files:
        try:
            with open(file_path, "r") as f:
                for line_num, line in enumerate(f, 1):
                    search_line = line if case_sensitive else line.lower()
                    if search_pattern in search_line:
                        click.echo(f"{file_path}:{line_num}:{line.rstrip()}")
        except Exception as e:
            click.echo(f"Error reading {file_path}: {e}", err=True)


@click.command()
@click.option("--format", type=click.Choice(["json", "text", "csv"]), default="text")
@click.option("--output", "-o", type=click.Path(), help="Output file")
def data_processor(format: str, output: Optional[str]) -> None:
    """Process data in different formats."""
    sample_data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "San Francisco"},
        {"name": "Charlie", "age": 35, "city": "Chicago"},
    ]

    if format == "json":
        import json

        output_text = json.dumps(sample_data, indent=2)
    elif format == "csv":
        import csv
        import io

        output_buffer = io.StringIO()
        if sample_data:
            writer = csv.DictWriter(output_buffer, fieldnames=sample_data[0].keys())
            writer.writeheader()
            writer.writerows(sample_data)
        output_text = output_buffer.getvalue()
    else:  # text
        output_text = "\n".join(
            f"{item['name']}, {item['age']}, {item['city']}" for item in sample_data
        )

    if output:
        with open(output, "w") as f:
            f.write(output_text)
        click.echo(f"Data written to {output}")
    else:
        click.echo(output_text)


@click.command()
@click.confirmation_option(prompt="Are you sure you want to proceed?")
def dangerous_command() -> None:
    """A command that requires confirmation."""
    click.echo("Dangerous operation executed!")


@click.command()
@click.option("--timeout", default=5, help="Timeout in seconds")
def slow_command(timeout: int) -> None:
    """A command that takes time to execute."""
    import time

    click.echo(f"Starting slow operation (timeout: {timeout}s)...")
    time.sleep(min(timeout, 2))  # Never sleep more than 2 seconds in tests
    click.echo("Slow operation completed!")


if __name__ == "__main__":
    hello()
