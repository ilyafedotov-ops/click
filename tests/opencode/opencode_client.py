"""Opencode client for GLM-4.6 integration testing."""

import os
import json
import time
import logging
import urllib.request
import urllib.parse
import urllib.error
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class OpencodeConfig:
    """Configuration for opencode GLM-4.6 client."""

    api_base_url: str = "https://api.opencode.ai/v1"
    model: str = "glm-4.6"
    api_key: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    session_id: Optional[str] = None

    @classmethod
    def from_env(cls) -> "OpencodeConfig":
        """Create configuration from environment variables."""
        return cls(
            api_base_url=os.getenv("OPENCODE_API_BASE_URL", cls.api_base_url),
            model=os.getenv("OPENCODE_MODEL", cls.model),
            api_key=os.getenv("OPENCODE_API_KEY"),
            timeout=int(os.getenv("OPENCODE_TIMEOUT", str(cls.timeout))),
            max_retries=int(os.getenv("OPENCODE_MAX_RETRIES", str(cls.max_retries))),
            retry_delay=float(os.getenv("OPENCODE_RETRY_DELAY", str(cls.retry_delay))),
            session_id=os.getenv("OPENCODE_SESSION_ID"),
        )


@dataclass
class OpencodeRequest:
    """Request payload for opencode API."""

    prompt: str
    max_tokens: Optional[int] = 2048
    temperature: float = 0.7
    stream: bool = False
    context: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        data = asdict(self)
        if self.context:
            data["context"] = self.context
        return data


@dataclass
class OpencodeResponse:
    """Response from opencode API."""

    content: str
    usage: Dict[str, int]
    model: str
    session_id: str
    finish_reason: str
    response_time: float

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], response_time: float
    ) -> "OpencodeResponse":
        """Create response from API data."""
        return cls(
            content=data.get("content", ""),
            usage=data.get("usage", {}),
            model=data.get("model", ""),
            session_id=data.get("session_id", ""),
            finish_reason=data.get("finish_reason", ""),
            response_time=response_time,
        )


class OpencodeClientError(Exception):
    """Base exception for opencode client errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class OpencodeAuthenticationError(OpencodeClientError):
    """Authentication error for opencode API."""

    pass


class OpencodeRateLimitError(OpencodeClientError):
    """Rate limit error for opencode API."""

    pass


class OpencodeClient:
    """Client for interacting with opencode GLM-4.6 API."""

    def __init__(self, config: Optional[OpencodeConfig] = None):
        """Initialize the opencode client.

        Args:
            config: Configuration for the client. If None, loads from environment.
        """
        self.config = config or OpencodeConfig.from_env()
        self.logger = logging.getLogger(__name__)

        if not self.config.api_key:
            # For testing, allow mock mode without API key
            if os.getenv("OPENCODE_MOCK_MODE", "false").lower() == "true":
                self.mock_mode = True
            else:
                raise OpencodeAuthenticationError("API key is required")
        else:
            self.mock_mode = False

    def _make_request_with_retry(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make HTTP request to opencode API with retry logic."""
        if self.mock_mode:
            return self._mock_response(data)

        url = f"{self.config.api_base_url}/{endpoint}"
        json_data = json.dumps(data).encode("utf-8")

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(self.config.max_retries + 1):
            try:
                start_time = time.time()

                req = urllib.request.Request(
                    url, data=json_data, headers=headers, method="POST"
                )

                with urllib.request.urlopen(
                    req, timeout=self.config.timeout
                ) as response:
                    response_time = time.time() - start_time

                    if response.status == 401:
                        raise OpencodeAuthenticationError(
                            "Invalid API key", response.status
                        )
                    elif response.status == 429:
                        raise OpencodeRateLimitError(
                            "Rate limit exceeded", response.status
                        )
                    elif response.status >= 400:
                        error_text = response.read().decode("utf-8")
                        raise OpencodeClientError(
                            f"API error: {error_text}", response.status
                        )

                    result = json.loads(response.read().decode("utf-8"))
                    result["response_time"] = response_time
                    return result

            except urllib.error.URLError as e:
                if attempt == self.config.max_retries:
                    raise OpencodeClientError(
                        f"Network error after {attempt + 1} attempts: {str(e)}"
                    )
                time.sleep(self.config.retry_delay * (2**attempt))
            except (OpencodeRateLimitError, OpencodeClientError) as e:
                if attempt == self.config.max_retries:
                    raise
                time.sleep(self.config.retry_delay * (2**attempt))

        # This should not be reached, but just in case
        raise OpencodeClientError("Failed to complete request after all retries")

    def _mock_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock response for testing."""
        prompt = data.get("prompt", "")

        # Simple mock responses based on prompt content
        if "execute this CLI command" in prompt.lower():
            content = """
To execute the CLI command, use the following syntax:

1. Basic command structure: `command [options] [arguments]`
2. For click commands, use `python -m module.command`
3. Common options: `--help`, `--version`, `--verbose`

Example usage:
```bash
python -m your_module.command --option value argument
```

Expected output will depend on the specific command and options used.
            """.strip()
        elif "trouble with this CLI command" in prompt.lower():
            content = """
Based on the error, here are the most common issues and solutions:

1. **Syntax Error**: Check command spelling and argument order
2. **Missing Options**: Add required options with `--option value`
3. **Permission Issues**: Use appropriate permissions or sudo
4. **Path Issues**: Ensure the command is in your PATH

Corrected command example:
```bash
python -m your_module.command --required-option value
```

The error typically occurs when required parameters are missing or incorrectly formatted.
            """.strip()
        else:
            content = "I understand you need help with CLI operations. Please provide more specific details about the command or issue you're experiencing."

        return {
            "content": content,
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 150,
                "total_tokens": 250,
            },
            "model": self.config.model,
            "session_id": self.config.session_id or "mock_session",
            "finish_reason": "stop",
            "response_time": 0.5,
        }

    def generate_response(self, request: OpencodeRequest) -> OpencodeResponse:
        """Generate response from opencode GLM-4.6.

        Args:
            request: The request to send to the API

        Returns:
            OpencodeResponse with the generated content
        """
        data = request.to_dict()

        if self.config.session_id:
            data["session_id"] = self.config.session_id

        try:
            result = self._make_request_with_retry("chat/completions", data)
            return OpencodeResponse.from_dict(result, result.get("response_time", 0))

        except Exception as e:
            self.logger.error(f"Failed to generate response: {str(e)}")
            raise

    def execute_cli_command(
        self, command: str, context: Optional[Dict[str, Any]] = None
    ) -> OpencodeResponse:
        """Execute CLI command through opencode assistance.

        Args:
            command: CLI command to execute or get help with
            context: Additional context for command execution

        Returns:
            OpencodeResponse with command assistance
        """
        prompt = f"""
        Help me execute this CLI command: {command}
        
        Please provide:
        1. The correct command syntax
        2. Any required parameters or options
        3. Example usage
        4. Expected output format
        
        If this is a click command, consider click-specific patterns and conventions.
        """

        request = OpencodeRequest(
            prompt=prompt,
            context=context or {},
            temperature=0.3,  # Lower temperature for more consistent CLI help
        )

        return self.generate_response(request)

    def debug_cli_issue(
        self, command: str, error_output: str, context: Optional[Dict[str, Any]] = None
    ) -> OpencodeResponse:
        """Debug CLI command issues with opencode assistance.

        Args:
            command: The CLI command that failed
            error_output: Error message or output from the failed command
            context: Additional context about the environment

        Returns:
            OpencodeResponse with debugging assistance
        """
        prompt = f"""
        I'm having trouble with this CLI command: {command}
        
        Error output:
        {error_output}
        
        Please help me:
        1. Identify the root cause of the error
        2. Suggest fixes or workarounds
        3. Provide the corrected command syntax
        4. Explain why the error occurred
        """

        request = OpencodeRequest(
            prompt=prompt,
            context=context or {},
            temperature=0.4,
        )

        return self.generate_response(request)


class OpencodeClientFactory:
    """Factory for creating opencode clients with test isolation."""

    _default_config: Optional[OpencodeConfig] = None

    @classmethod
    def set_default_config(cls, config: OpencodeConfig):
        """Set default configuration for all clients."""
        cls._default_config = config

    @classmethod
    def create_client(
        cls, config: Optional[OpencodeConfig] = None, session_id: Optional[str] = None
    ) -> OpencodeClient:
        """Create a new opencode client.

        Args:
            config: Configuration for the client. Uses default if None.
            session_id: Session ID for the client

        Returns:
            New OpencodeClient instance
        """
        client_config = config or cls._default_config or OpencodeConfig.from_env()

        if session_id:
            client_config.session_id = session_id

        return OpencodeClient(client_config)

    @classmethod
    def create_isolated_client(cls, test_name: str) -> OpencodeClient:
        """Create an isolated client for testing.

        Args:
            test_name: Name of the test for isolation

        Returns:
            New OpencodeClient with isolated session
        """
        session_id = f"test_{test_name}_{int(time.time())}"
        return cls.create_client(session_id=session_id)
