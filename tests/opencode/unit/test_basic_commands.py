"""Tests for basic click commands."""

import pytest
from ..helpers.cli_client import OpencodeTestClient
from ..helpers.assertions import CLIAssertions
from ..helpers.mocks import mock_stdin


class TestBasicCommands:
    """Test basic command execution scenarios."""

    def test_simple_command_execution(
        self, opencode_client: OpencodeTestClient, sample_command_file
    ):
        """Test simple command invocation."""
        result = opencode_client.run_python_script(
            sample_command_file, ["--name", "World", "--count", "1"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello World!")

    def test_help_text_display(
        self, opencode_client: OpencodeTestClient, sample_command_file
    ):
        """Test help text display."""
        result = opencode_client.run_python_script(sample_command_file, ["--help"])
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Simple program that greets")
        CLIAssertions.assert_output_contains(result, "--count")
        CLIAssertions.assert_output_contains(result, "--name")
        CLIAssertions.assert_output_contains(result, "--verbose")

    def test_command_with_prompt(
        self, opencode_client: OpencodeTestClient, sample_command_file
    ):
        """Test command with user input prompt."""
        with mock_stdin(["Alice"]):
            result = opencode_client.run_python_script(
                sample_command_file, ["--count", "2"]
            )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello Alice!")
        CLIAssertions.assert_line_count(result, 2)  # Two greetings

    def test_verbose_flag(
        self, opencode_client: OpencodeTestClient, sample_command_file
    ):
        """Test verbose flag functionality."""
        result = opencode_client.run_python_script(
            sample_command_file, ["--name", "Bob", "--count", "1", "--verbose"]
        )
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Starting greeting process")
        CLIAssertions.assert_output_contains(result, "Greeting process completed")

    def test_default_values(
        self, opencode_client: OpencodeTestClient, sample_command_file
    ):
        """Test default option values."""
        with mock_stdin(["Charlie"]):
            result = opencode_client.run_python_script(sample_command_file)
        CLIAssertions.assert_success(result)
        CLIAssertions.assert_output_contains(result, "Hello Charlie!")
        # Should only have one greeting (default count=1)
        CLIAssertions.assert_line_count(result, 1)
