"""Mock utilities for opencode click testing."""

import os
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Iterator
from unittest.mock import MagicMock, patch
import json


class FileSystemMock:
    """Mock file system operations for CLI testing."""

    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize file system mock.

        Args:
            base_dir: Base directory for mock operations
        """
        self.base_dir = base_dir or Path(tempfile.mkdtemp())
        self.files: Dict[str, str] = {}
        self.directories: set[str] = set()

    def create_file(self, path: Union[str, Path], content: str = "") -> Path:
        """Create a mock file with content."""
        file_path = self.base_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        self.files[str(file_path)] = content
        return file_path

    def create_directory(self, path: Union[str, Path]) -> Path:
        """Create a mock directory."""
        dir_path = self.base_dir / path
        dir_path.mkdir(parents=True, exist_ok=True)
        self.directories.add(str(dir_path))
        return dir_path

    def get_file_path(self, path: Union[str, Path]) -> Path:
        """Get full path for a mock file."""
        return self.base_dir / path

    def cleanup(self) -> None:
        """Clean up mock file system."""
        import shutil

        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)


class EnvironmentMock:
    """Mock environment variables for CLI testing."""

    def __init__(self):
        """Initialize environment mock."""
        self.original_env: Dict[str, str] = {}
        self.mock_env: Dict[str, str] = {}

    def set(self, key: str, value: str) -> None:
        """Set a mock environment variable."""
        if key not in self.mock_env and key in os.environ:
            self.original_env[key] = os.environ[key]
        self.mock_env[key] = value
        os.environ[key] = value

    def unset(self, key: str) -> None:
        """Unset an environment variable."""
        if key in os.environ:
            if key not in self.original_env:
                self.original_env[key] = os.environ[key]
            del os.environ[key]
        self.mock_env.pop(key, None)

    def restore(self) -> None:
        """Restore original environment variables."""
        for key in self.mock_env:
            if key in self.original_env:
                os.environ[key] = self.original_env[key]
            else:
                os.environ.pop(key, None)
        self.original_env.clear()
        self.mock_env.clear()


class StdinMock:
    """Mock stdin for CLI testing."""

    def __init__(self, inputs: List[str]):
        """Initialize stdin mock with list of inputs.

        Args:
            inputs: List of strings to provide as stdin input
        """
        self.inputs = iter(inputs)
        self.current_input = ""

    def __call__(self, prompt: str = "") -> str:
        """Mock input function."""
        try:
            self.current_input = next(self.inputs)
            return self.current_input
        except StopIteration:
            raise EOFError("No more input available")


class ClickCommandMock:
    """Mock Click command for testing."""

    def __init__(self, name: str, callback=None):
        """Initialize mock command.

        Args:
            name: Command name
            callback: Optional callback function
        """
        self.name = name
        self.callback = callback or (lambda: None)
        self.params = []
        self.help_text = f"Mock command: {name}"

    def add_param(self, param_type: str, name: str, **kwargs) -> None:
        """Add a parameter to the mock command."""
        self.params.append({"type": param_type, "name": name, **kwargs})

    def invoke(self, *args, **kwargs) -> Any:
        """Invoke the mock command."""
        return self.callback(*args, **kwargs)


class MockContext:
    """Mock Click context for testing."""

    def __init__(self, command_name: str = "test", parent=None):
        """Initialize mock context.

        Args:
            command_name: Name of the command
            parent: Parent context
        """
        self.command_name = command_name
        self.parent = parent
        self.params = {}
        self.obj = {}
        self.info_name = command_name
        self.invoked_subcommand = None

    def set_param(self, key: str, value: Any) -> None:
        """Set a context parameter."""
        self.params[key] = value

    def get_param(self, key: str, default: Any = None) -> Any:
        """Get a context parameter."""
        return self.params.get(key, default)


def mock_click_command(name: str, help_text: Optional[str] = None):
    """Decorator to create mock Click commands."""

    def decorator(func):
        mock_cmd = MagicMock()
        mock_cmd.name = name
        mock_cmd.callback = func
        mock_cmd.help = help_text or f"Mock command: {name}"
        mock_cmd.params = []
        return mock_cmd

    return decorator


def mock_file_system(
    files: Dict[str, str], directories: Optional[List[str]] = None
) -> Iterator[FileSystemMock]:
    """Context manager to mock file system."""
    fs_mock = FileSystemMock()
    try:
        for path, content in files.items():
            fs_mock.create_file(path, content)
        for dir_path in directories or []:
            fs_mock.create_directory(dir_path)
        yield fs_mock
    finally:
        fs_mock.cleanup()


def mock_environment(env_vars: Dict[str, str]) -> Iterator[EnvironmentMock]:
    """Context manager to mock environment variables."""
    env_mock = EnvironmentMock()
    try:
        for key, value in env_vars.items():
            env_mock.set(key, value)
        yield env_mock
    finally:
        env_mock.restore()


def mock_stdin(inputs: List[str]) -> Iterator[StdinMock]:
    """Context manager to mock stdin input."""
    stdin_mock = StdinMock(inputs)
    with patch("builtins.input", stdin_mock):
        yield stdin_mock


def create_mock_config(config_data: Dict[str, Any]) -> Path:
    """Create a mock configuration file."""
    config_file = Path(tempfile.mktemp(suffix=".json"))
    config_file.write_text(json.dumps(config_data, indent=2))
    return config_file
