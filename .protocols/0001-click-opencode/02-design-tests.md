# Step 2: Design test framework

## Briefing
- **Goal:** Create a comprehensive test architecture for opencode glm-4.6 integration
- **Key files:**
  - `tests/` (existing test structure)
  - New test framework files to be created
- **Additional info:** Design tests that work with opencode's CLI interaction patterns

## Sub-tasks

### 1. Design test architecture
1.1. Create directory structure `tests/opencode/` with subdirectories:
   - `tests/opencode/integration/` - End-to-end CLI tests
   - `tests/opencode/unit/` - Individual component tests
   - `tests/opencode/fixtures/` - Test data and mock files
   - `tests/opencode/helpers/` - Shared test utilities

1.2. Define test categories and naming conventions:
   - Basic command tests: `test_basic_commands.py`
   - Option handling tests: `test_options.py`
   - Group/subcommand tests: `test_groups.py`
   - Error handling tests: `test_errors.py`
   - Integration tests: `test_integration.py`

1.3. Design opencode integration layer:
   - Create `tests/opencode/conftest.py` for pytest fixtures
   - Define `OpencodeTestClient` class for CLI interactions
   - Design response validation patterns

### 2. Create test utilities
2.1. Build CLI interaction helpers:
   - Create `tests/opencode/helpers/cli_client.py` with `OpencodeTestClient`
   - Implement command execution methods with timeout handling
   - Add output parsing and validation utilities

2.2. Create assertion utilities:
   - Create `tests/opencode/helpers/assertions.py`
   - Implement CLI output comparison functions
   - Add exit code validation helpers
   - Create error message assertion utilities

2.3. Design mock/stub patterns:
   - Create `tests/opencode/helpers/mocks.py`
   - Implement file system mocks for CLI operations
   - Design environment variable mocking utilities
   - Create stdin/stdout capture mechanisms

### 3. Plan test scenarios
3.1. Basic command execution tests:
   - Test simple command invocation
   - Verify help text display
   - Test version command functionality
   - Validate command discovery

3.2. Option parsing and validation tests:
   - Test required vs optional options
   - Validate option type conversion
   - Test default value handling
   - Verify option conflict detection

3.3. Group and subcommand tests:
   - Test command group creation
   - Verify subcommand routing
   - Test nested group structures
   - Validate help text for groups

3.4. Error handling and edge cases:
   - Test invalid command invocation
   - Verify error message formatting
   - Test exception propagation
   - Validate graceful failure modes

3.5. Integration scenarios with opencode glm-4.6:
   - Test opencode tool integration
   - Verify model interaction patterns
   - Test async command handling
   - Validate complex workflow scenarios

### 4. Create test configuration
4.1. Set up pytest configuration:
   - Create `tests/opencode/pytest.ini` or update root configuration
   - Define test markers for different test categories
   - Configure test discovery patterns
   - Set up coverage reporting

4.2. Define test data fixtures:
   - Create `tests/opencode/fixtures/sample_commands.py`
   - Add mock CLI command definitions
   - Create test input/output data files
   - Set up environment configuration fixtures

4.3. Configure test environment:
   - Create `tests/opencode/.env.test` for test-specific variables
   - Define opencode model configuration
   - Set up temporary directory management
   - Configure logging for test execution

## Workflow
1. Execute sub-tasks in order.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(design): create opencode test framework [protocol-0001/02]"`. Push.
5. Report to user using the step report format above.