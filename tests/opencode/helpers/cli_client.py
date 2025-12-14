"""CLI client for opencode click testing."""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import json


class OpencodeTestClient:
    """Client for testing CLI commands with opencode integration."""

    def __init__(self, timeout: int = 30, work_dir: Optional[Path] = None):
        """Initialize the CLI test client.

        Args:
            timeout: Command execution timeout in seconds
            work_dir: Working directory for command execution
        """
        self.timeout = timeout
        self.work_dir = work_dir or Path.cwd()
        self.env = {}

    def run_command(
        self,
        command: Union[str, List[str]],
        input_data: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        capture_output: bool = True,
        check: bool = False,
    ) -> subprocess.CompletedProcess:
        """Run a CLI command and return the result.

        Args:
            command: Command to execute (string or list)
            input_data: Data to send to stdin
            env: Environment variables to set
            capture_output: Whether to capture stdout/stderr
            check: Whether to raise exception on non-zero exit

        Returns:
            CompletedProcess with command results
        """
        if isinstance(command, str):
            cmd_list = command.split()
        else:
            cmd_list = command

        cmd_env = os.environ.copy()
        cmd_env.update(self.env)
        if env:
            cmd_env.update(env)

        try:
            result = subprocess.run(
                cmd_list,
                cwd=self.work_dir,
                timeout=self.timeout,
                input=input_data,
                env=cmd_env,
                capture_output=capture_output,
                text=True,
                check=check,
            )
            return result
        except subprocess.TimeoutExpired as e:
            raise TimeoutError(
                f"Command timed out after {self.timeout}s: {' '.join(cmd_list)}"
            ) from e

    def run_python_script(
        self, script_path: Path, args: Optional[List[str]] = None, **kwargs
    ) -> subprocess.CompletedProcess:
        """Run a Python script using the current interpreter.

        Args:
            script_path: Path to the Python script
            args: Command line arguments for the script
            **kwargs: Additional arguments passed to run_command

        Returns:
            CompletedProcess with execution results
        """
        command = ["python", str(script_path)]
        if args:
            command.extend(args)
        return self.run_command(command, **kwargs)

    def run_click_command(
        self, module_path: str, command_args: Optional[List[str]] = None, **kwargs
    ) -> subprocess.CompletedProcess:
        """Run a click command using python -m.

        Args:
            module_path: Python module path (e.g., 'my_module.cli')
            command_args: Arguments to pass to the command
            **kwargs: Additional arguments passed to run_command

        Returns:
            CompletedProcess with execution results
        """
        command = ["python", "-m", module_path]
        if command_args:
            command.extend(command_args)
        return self.run_command(command, **kwargs)

    def assert_success(self, result: subprocess.CompletedProcess) -> None:
        """Assert that the command succeeded."""
        if result.returncode != 0:
            raise AssertionError(
                f"Command failed with exit code {result.returncode}: {result.stderr}"
            )

    def assert_failure(
        self, result: subprocess.CompletedProcess, expected_code: Optional[int] = None
    ) -> None:
        """Assert that the command failed."""
        if result.returncode == 0:
            raise AssertionError("Command succeeded but was expected to fail")
        if expected_code is not None and result.returncode != expected_code:
            raise AssertionError(
                f"Command failed with exit code {result.returncode}, expected {expected_code}"
            )

    def assert_output_contains(
        self, result: subprocess.CompletedProcess, text: str
    ) -> None:
        """Assert that stdout contains the expected text."""
        if text not in result.stdout:
            raise AssertionError(f"Expected '{text}' in stdout, got: {result.stdout}")

    def assert_error_contains(
        self, result: subprocess.CompletedProcess, text: str
    ) -> None:
        """Assert that stderr contains the expected text."""
        if text not in result.stderr:
            raise AssertionError(f"Expected '{text}' in stderr, got: {result.stderr}")

    def get_json_output(self, result: subprocess.CompletedProcess) -> Dict[str, Any]:
        """Parse JSON output from command."""
        try:
            return json.loads(result.stdout.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {result.stdout}") from e
