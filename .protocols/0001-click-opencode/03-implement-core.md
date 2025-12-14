# Step 3: Implement core tests

## Briefing
- **Goal:** Build fundamental CLI test cases for basic click functionality
- **Key files:**
  - `tests/opencode/test_basic_commands.py`
  - `tests/opencode/test_options.py`
  - `tests/opencode/conftest.py`
- **Additional info:** Focus on core click features that are commonly used

## Sub-tasks
1. **Create test directory structure and conftest.py:**
   - Create `tests/opencode/` directory if it doesn't exist
   - Implement `conftest.py` with shared fixtures and utilities
   - Add CLI execution helper functions
   - Add output parsing utilities
   - Add error assertion helpers

2. **Implement basic command tests:**
   - Create `test_basic_commands.py` file
   - Test simple command execution with various click decorators
   - Test command help output formatting and content
   - Test command version information display
   - Test command error handling for invalid inputs
   - Test command name resolution and invocation

3. **Create option parsing tests:**
   - Create `test_options.py` file
   - Test required vs optional options with different parameter types
   - Test option type conversion (int, float, bool, string, choice)
   - Test option default values and fallback behavior
   - Test multiple option combinations and precedence
   - Test option validation and custom validators
   - Test flag options and counting options

4. **Build argument handling tests:**
   - Create `test_arguments.py` file
   - Test positional arguments with type conversion
   - Test argument validation and custom validators
   - Test argument count constraints (min, max, exact)
   - Test variadic arguments and nargs behavior
   - Test argument help generation and display

5. **Add comprehensive test coverage:**
   - Test edge cases and boundary conditions
   - Test Unicode and special character handling
   - Test environment variable integration
   - Test callback functions and context usage
   - Test command chaining and group functionality

6. **Create integration test utilities:**
   - Add mock CLI commands for testing
   - Add temporary file/directory helpers
   - Add process execution utilities
   - Add assertion helpers for CLI output patterns

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(tests): implement core CLI tests [protocol-0001/03]"`. Push.
5. Report to user using the step report format above.