"""Test categories and naming conventions for opencode click testing."""

# Test file naming conventions:
# - Basic command tests: test_basic_commands.py
# - Option handling tests: test_options.py
# - Group/subcommand tests: test_groups.py
# - Error handling tests: test_errors.py
# - Integration tests: test_integration.py

# Test markers for pytest:
# - basic: Basic command execution tests
# - options: Option parsing and validation tests
# - groups: Group and subcommand tests
# - errors: Error handling and edge cases
# - integration: Integration scenarios with opencode glm-4.6
# - slow: Tests that take longer to execute

# Test structure patterns:
# - test_<functionality>_<scenario> for specific test cases
# - Given-When-Then pattern for complex scenarios
# - Parametrized tests for multiple input variations
