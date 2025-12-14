# Step 3: Implement core tests

## Briefing
- **Goal:** Build basic CLI functionality tests using opencode framework
- **Key files:**
  - `tests/opencode/unit/test_basic_commands.py`
  - `tests/opencode/fixtures/sample_commands.py`
  - `tests/opencode/opencode_client.py`
- **Additional info:** Focus on fundamental Click CLI features: simple commands, options, arguments, and help system

## Sub-tasks
1. **Create sample CLI commands foundation:**
   - Create `tests/opencode/fixtures/sample_commands.py` with basic Click command examples
   - Implement simple greeting command with string argument
   - Add calculator command with numeric operations
   - Include file processing command with path argument
   - Add command with multiple options and flags

2. **Implement CLI runner utilities:**
   - Create `tests/opencode/helpers/cli_runner.py` with Click testing utilities
   - Add command execution wrapper with output capture
   - Implement error handling and timeout management
   - Add assertion helpers for CLI output validation
   - Include utilities for testing command exit codes

3. **Build opencode client integration:**
   - Complete `tests/opencode/opencode_client.py` with glm-4.6 API integration
   - Implement test scenario generation based on command definitions
   - Add response parsing and validation logic
   - Include error handling for API failures
   - Add logging and debugging capabilities

4. **Implement basic command execution tests:**
   - Create `tests/opencode/unit/test_basic_commands.py` with test infrastructure
   - Test simple command execution with valid arguments
   - Test command help functionality and output validation
   - Test error handling for invalid arguments and missing parameters
   - Test command exit codes and standard error output

5. **Test options and arguments handling:**
   - Implement tests for string, integer, boolean, and flag options
   - Test required vs optional arguments with various combinations
   - Test default values and parameter validation
   - Test multiple value options and choice constraints
   - Test option parsing edge cases and error messages

6. **Add comprehensive assertion helpers:**
   - Create `tests/opencode/helpers/assertions.py` with custom assertions
   - Add output format validation helpers
   - Include regex-based content matching
   - Add performance and timeout assertions
   - Implement CLI-specific error message validation

7. **Create test configuration and fixtures:**
   - Update `tests/opencode/conftest.py` with shared fixtures
   - Add pytest configuration for opencode tests
   - Create test data files for file processing tests
   - Set up environment variables and test isolation
   - Add cleanup utilities for test artifacts

## Workflow
1. Execute sub-tasks in order.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(tests): implement core CLI functionality tests [protocol-0001/03]"`. Push.
5. Report to user using the step report format above.