"""CLI interaction helpers for opencode testing."""

import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import json


class CLIResult:
    """Result of a CLI command execution."""

    def __init__(
        self,
        stdout: str,
        stderr: str,
        exit_code: int,
        command: List[str],
        duration: float,
    ):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code
        self.command = command
        self.duration = duration

    @property
    def success(self) -> bool:
        """Check if command executed successfully."""
        return self.exit_code == 0

    @property
    def output(self) -> str:
        """Get combined output."""
        return self.stdout + self.stderr

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "stdout": self.stdout,
            "stderr": self.stderr,
            "exit_code": self.exit_code,
            "command": self.command,
            "duration": self.duration,
            "success": self.success,
        }


class OpencodeTestClient:
    """Test client for CLI interactions with opencode integration."""

    def __init__(self, timeout: int = 30, work_dir: Optional[Path] = None):
        self.timeout = timeout
        self.work_dir = work_dir or Path.cwd()
        self.env_vars = {}

    def set_env_var(self, key: str, value: str) -> None:
        """Set environment variable for commands."""
        self.env_vars[key] = value

    def clear_env_vars(self) -> None:
        """Clear all environment variables."""
        self.env_vars.clear()

    def run_command(
        self,
        command: Union[str, List[str]],
        input_data: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        capture_output: bool = True,
        check: bool = False,
    ) -> CLIResult:
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
        cmd_env.update(self.env_vars)
        if env:
            cmd_env.update(env)

        start_time = time.time()

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

            duration = time.time() - start_time

            cli_result = CLIResult(
                stdout=result.stdout or "",
                stderr=result.stderr or "",
                exit_code=result.returncode,
                command=cmd_list,
                duration=duration,
            )

            return cli_result

        except subprocess.TimeoutExpired as e:
            duration = time.time() - start_time
            return CLIResult(
                stdout="",
                stderr=f"Command timed out after {self.timeout} seconds",
                exit_code=124,
                command=cmd_list,
                duration=duration,
            )

    def run_python_script(
        self, script_path: Path, args: Optional[List[str]] = None, **kwargs
    ) -> CLIResult:
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
    ) -> CLIResult:
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

    def assert_success(self, result: CLIResult) -> None:
        """Assert that the command succeeded."""
        if result.exit_code != 0:
            raise AssertionError(
                f"Command failed with exit code {result.exit_code}: {result.stderr}"
            )

    def assert_failure(
        self, result: CLIResult, expected_code: Optional[int] = None
    ) -> None:
        """Assert that the command failed."""
        if result.exit_code == 0:
            raise AssertionError("Command succeeded but was expected to fail")
        if expected_code is not None and result.exit_code != expected_code:
            raise AssertionError(
                f"Command failed with exit code {result.exit_code}, expected {expected_code}"
            )

    def assert_output_contains(self, result: CLIResult, text: str) -> None:
        """Assert that stdout contains the expected text."""
        if text not in result.stdout:
            raise AssertionError(f"Expected '{text}' in stdout, got: {result.stdout}")

    def assert_error_contains(self, result: CLIResult, text: str) -> None:
        """Assert that stderr contains the expected text."""
        if text not in result.stderr:
            raise AssertionError(f"Expected '{text}' in stderr, got: {result.stderr}")

    def get_json_output(self, result: CLIResult) -> Dict[str, Any]:
        """Parse JSON output from command."""
        try:
            return json.loads(result.stdout.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON output: {result.stdout}") from e
