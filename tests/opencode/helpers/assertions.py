"""Assertion utilities for opencode click testing."""

import re
from typing import Optional, List, Union
import subprocess


class CLIAssertions:
    """Collection of assertion helpers for CLI testing."""

    @staticmethod
    def assert_exit_code(
        result: subprocess.CompletedProcess, expected_code: int = 0
    ) -> None:
        """Assert command exited with expected code."""
        if result.returncode != expected_code:
            raise AssertionError(
                f"Expected exit code {expected_code}, got {result.returncode}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )

    @staticmethod
    def assert_success(result: subprocess.CompletedProcess) -> None:
        """Assert command succeeded (exit code 0)."""
        CLIAssertions.assert_exit_code(result, 0)

    @staticmethod
    def assert_failure(
        result: subprocess.CompletedProcess, expected_code: Optional[int] = None
    ) -> None:
        """Assert command failed."""
        if result.returncode == 0:
            raise AssertionError("Command succeeded but was expected to fail")
        if expected_code is not None and result.returncode != expected_code:
            raise AssertionError(
                f"Expected exit code {expected_code}, got {result.returncode}"
            )

    @staticmethod
    def assert_output_contains(
        result: subprocess.CompletedProcess, text: str, case_sensitive: bool = True
    ) -> None:
        """Assert stdout contains expected text."""
        output = result.stdout
        if not case_sensitive:
            output = output.lower()
            text = text.lower()
        if text not in output:
            raise AssertionError(f"Expected '{text}' in stdout, got:\n{output}")

    @staticmethod
    def assert_output_not_contains(
        result: subprocess.CompletedProcess, text: str, case_sensitive: bool = True
    ) -> None:
        """Assert stdout does not contain text."""
        output = result.stdout
        if not case_sensitive:
            output = output.lower()
            text = text.lower()
        if text in output:
            raise AssertionError(f"Did not expect '{text}' in stdout, but it was found")

    @staticmethod
    def assert_error_contains(
        result: subprocess.CompletedProcess, text: str, case_sensitive: bool = True
    ) -> None:
        """Assert stderr contains expected text."""
        error_output = result.stderr
        if not case_sensitive:
            error_output = error_output.lower()
            text = text.lower()
        if text not in error_output:
            raise AssertionError(f"Expected '{text}' in stderr, got:\n{error_output}")

    @staticmethod
    def assert_output_matches(
        result: subprocess.CompletedProcess, pattern: str, flags: int = 0
    ) -> None:
        """Assert stdout matches regex pattern."""
        if not re.search(pattern, result.stdout, flags):
            raise AssertionError(
                f"Expected regex '{pattern}' to match stdout:\n{result.stdout}"
            )

    @staticmethod
    def assert_output_equals(
        result: subprocess.CompletedProcess, expected: str, strip: bool = True
    ) -> None:
        """Assert stdout exactly equals expected text."""
        actual = result.stdout
        expected_text = expected
        if strip:
            actual = actual.strip()
            expected_text = expected_text.strip()
        if actual != expected_text:
            raise AssertionError(f"Expected output:\n{expected_text}\n\nGot:\n{actual}")

    @staticmethod
    def assert_line_count(
        result: subprocess.CompletedProcess, expected_count: int
    ) -> None:
        """Assert stdout has expected number of lines."""
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        if len(lines) != expected_count:
            raise AssertionError(
                f"Expected {expected_count} lines, got {len(lines)}:\n{result.stdout}"
            )

    @staticmethod
    def assert_json_output(
        result: subprocess.CompletedProcess, expected_structure: dict
    ) -> None:
        """Assert stdout is valid JSON matching expected structure."""
        import json

        try:
            output_data = json.loads(result.stdout.strip())
        except json.JSONDecodeError as e:
            raise AssertionError(f"Output is not valid JSON: {e}")

        if not CLIAssertions._dict_matches_structure(output_data, expected_structure):
            raise AssertionError(
                f"JSON output {output_data} does not match expected structure {expected_structure}"
            )

    @staticmethod
    def _dict_matches_structure(data: dict, structure: dict) -> bool:
        """Check if dictionary matches expected structure."""
        if not isinstance(data, dict):
            return False

        for key, expected_value in structure.items():
            if key not in data:
                return False

            if isinstance(expected_value, dict):
                if not CLIAssertions._dict_matches_structure(data[key], expected_value):
                    return False
            elif isinstance(expected_value, list):
                if not isinstance(data[key], list):
                    return False
            elif expected_value != data[key] and expected_value is not None:
                return False

        return True

    @staticmethod
    def assert_help_text_contains(
        result: subprocess.CompletedProcess, sections: List[str]
    ) -> None:
        """Assert help text contains expected sections."""
        help_text = result.stdout
        for section in sections:
            if section not in help_text:
                raise AssertionError(
                    f"Expected help section '{section}' not found in:\n{help_text}"
                )

    @staticmethod
    def assert_option_in_help(
        result: subprocess.CompletedProcess, option_name: str
    ) -> None:
        """Assert an option is documented in help text."""
        help_text = result.stdout
        option_pattern = rf"(?:^|\s){re.escape(option_name)}\b"
        if not re.search(option_pattern, help_text, re.MULTILINE):
            raise AssertionError(
                f"Option '{option_name}' not found in help text:\n{help_text}"
            )

    @staticmethod
    def assert_command_in_help(
        result: subprocess.CompletedProcess, command_name: str
    ) -> None:
        """Assert a command is listed in help text."""
        help_text = result.stdout
        command_pattern = rf"(?:^|\s){re.escape(command_name)}\b"
        if not re.search(command_pattern, help_text, re.MULTILINE):
            raise AssertionError(
                f"Command '{command_name}' not found in help text:\n{help_text}"
            )
