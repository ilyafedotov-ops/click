"""Base test classes for opencode integration testing."""

import pytest
import tempfile
import os
from pathlib import Path
from typing import Generator, Any, Dict, Optional, List
from unittest.mock import Mock, patch

import sys
from pathlib import Path

# Add the opencode directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from opencode_client import (
    OpencodeClient,
    OpencodeConfig,
    OpencodeRequest,
    OpencodeResponse,
    OpencodeClientFactory,
    OpencodeAuthenticationError,
)


class BaseOpencodeTest:
    """Base class for opencode integration tests."""

    @pytest.fixture(autouse=True)
    def setup_opencode_mocks(self):
        """Set up mock environment for opencode tests."""
        # Enable mock mode for all tests
        os.environ["OPENCODE_MOCK_MODE"] = "true"

        # Mock API key if not set
        if "OPENCODE_API_KEY" not in os.environ:
            os.environ["OPENCODE_API_KEY"] = "test_mock_key"

        yield

        # Clean up
        os.environ.pop("OPENCODE_MOCK_MODE", None)

    @pytest.fixture
    def opencode_config(self) -> OpencodeConfig:
        """Create test opencode configuration."""
        return OpencodeConfig(
            api_key="test_key",
            model="glm-4.6",
            timeout=10,
            max_retries=2,
            session_id="test_session",
        )

    @pytest.fixture
    def opencode_client(self, opencode_config: OpencodeConfig) -> OpencodeClient:
        """Create opencode client for testing."""
        return OpencodeClient(opencode_config)

    @pytest.fixture
    def isolated_client(self) -> OpencodeClient:
        """Create isolated client for test isolation."""
        return OpencodeClientFactory.create_isolated_client("test_isolation")

    def create_test_request(self, prompt: str = "Test prompt") -> OpencodeRequest:
        """Create a test opencode request."""
        return OpencodeRequest(
            prompt=prompt,
            max_tokens=100,
            temperature=0.5,
            context={"test": True},
        )

    def assert_valid_response(self, response: OpencodeResponse) -> None:
        """Assert that response is valid."""
        assert response.content is not None
        assert isinstance(response.content, str)
        assert len(response.content) > 0
        assert response.usage is not None
        assert isinstance(response.usage, dict)
        assert response.model is not None
        assert response.session_id is not None
        assert response.response_time >= 0


class OpencodeCommandTest(BaseOpencodeTest):
    """Base class for testing opencode command execution."""

    @pytest.fixture
    def sample_click_command(self) -> str:
        """Sample click command for testing."""
        return """
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    '''Simple program that greets NAME for a total of COUNT times.'''
    for _ in range(count):
        click.echo(f'Hello {name}!')

if __name__ == '__main__':
    hello()
        """.strip()

    @pytest.fixture
    def temp_script_file(self, sample_click_command: str, temp_dir: Path) -> Path:
        """Create temporary script file with sample command."""
        script_file = temp_dir / "sample_command.py"
        script_file.write_text(sample_click_command)
        return script_file

    def test_command_execution_help(self, opencode_client: OpencodeClient) -> None:
        """Test getting help for command execution."""
        response = opencode_client.execute_cli_command(
            "python sample_command.py --help"
        )

        self.assert_valid_response(response)
        assert "syntax" in response.content.lower()
        assert "option" in response.content.lower()

    def test_command_debugging(self, opencode_client: OpencodeClient) -> None:
        """Test debugging command issues."""
        response = opencode_client.debug_cli_issue(
            "python sample_command.py",
            "Error: Missing option '--name'",
        )

        self.assert_valid_response(response)
        assert "error" in response.content.lower()
        assert (
            "fix" in response.content.lower() or "solution" in response.content.lower()
        )


class OpencodeSessionTest(BaseOpencodeTest):
    """Base class for testing opencode session management."""

    def test_session_isolation(self) -> None:
        """Test that different clients have isolated sessions."""
        client1 = OpencodeClientFactory.create_isolated_client("test1")
        client2 = OpencodeClientFactory.create_isolated_client("test2")

        # Sessions should be different
        assert client1.config.session_id != client2.config.session_id

        # Both should work
        request1 = self.create_test_request("Test client 1")
        request2 = self.create_test_request("Test client 2")

        response1 = client1.generate_response(request1)
        response2 = client2.generate_response(request2)

        self.assert_valid_response(response1)
        self.assert_valid_response(response2)

        # Session IDs should be different in responses
        assert response1.session_id != response2.session_id

    def test_session_persistence(self, opencode_client: OpencodeClient) -> None:
        """Test that session persists across multiple requests."""
        request1 = self.create_test_request("First request")
        request2 = self.create_test_request("Second request")

        response1 = opencode_client.generate_response(request1)
        response2 = opencode_client.generate_response(request2)

        self.assert_valid_response(response1)
        self.assert_valid_response(response2)

        # Session ID should be the same
        assert response1.session_id == response2.session_id


class OpencodeErrorTest(BaseOpencodeTest):
    """Base class for testing opencode error handling."""

    def test_authentication_error(self) -> None:
        """Test authentication error handling."""
        # Remove API key and disable mock mode
        original_mock = os.environ.get("OPENCODE_MOCK_MODE")
        original_key = os.environ.get("OPENCODE_API_KEY")

        try:
            os.environ.pop("OPENCODE_MOCK_MODE", None)
            os.environ.pop("OPENCODE_API_KEY", None)

            with pytest.raises(OpencodeAuthenticationError):
                OpencodeClient()
        finally:
            if original_mock:
                os.environ["OPENCODE_MOCK_MODE"] = original_mock
            if original_key:
                os.environ["OPENCODE_API_KEY"] = original_key

    def test_invalid_request_handling(self, opencode_client: OpencodeClient) -> None:
        """Test handling of invalid requests."""
        # Test with empty prompt
        request = OpencodeRequest(prompt="", max_tokens=0)
        response = opencode_client.generate_response(request)

        # Should still return a valid response in mock mode
        self.assert_valid_response(response)


class OpencodePerformanceTest(BaseOpencodeTest):
    """Base class for testing opencode performance characteristics."""

    def test_response_time(self, opencode_client: OpencodeClient) -> None:
        """Test response time is within acceptable limits."""
        request = self.create_test_request("Performance test")

        response = opencode_client.generate_response(request)

        self.assert_valid_response(response)

        # In mock mode, response should be very fast
        assert response.response_time < 2.0

    def test_concurrent_requests(self) -> None:
        """Test handling of concurrent requests."""
        import threading
        import time

        client = OpencodeClientFactory.create_isolated_client("concurrent_test")
        results = []
        errors = []

        def make_request(request_id: int):
            try:
                request = self.create_test_request(f"Concurrent request {request_id}")
                response = client.generate_response(request)
                results.append((request_id, response))
            except Exception as e:
                errors.append((request_id, e))

        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request, args=(i,))
            threads.append(thread)

        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        end_time = time.time()

        # Verify results
        assert len(errors) == 0, f"Errors occurred: {errors}"
        assert len(results) == 5

        # All responses should be valid
        for request_id, response in results:
            self.assert_valid_response(response)

        # Should complete in reasonable time
        assert end_time - start_time < 10.0
