# Step 4: Advanced scenarios

## Briefing
- **Goal:** Test complex CLI interactions, error handling, and edge cases
- **Key files:**
  - `tests/opencode/test_scenarios.py`
  - `examples/complex/complex/cli.py`
  - `examples/imagepipe/imagepipe.py`
  - `src/click/exceptions.py`
- **Additional info:** Focus on real-world CLI usage patterns and robustness

## Sub-tasks
1. **Test multi-command CLI interactions:**
   - Analyze `examples/complex/complex/cli.py` structure and command hierarchy
   - Create test functions for command group discovery and help
   - Test subcommand execution with various argument combinations
   - Test command context passing between parent and child commands
   - Test command chaining scenarios with multiple levels
   - Validate command inheritance and option propagation

2. **Test error handling and exceptions:**
   - Review `src/click/exceptions.py` and identify all exception types
   - Create test cases for `ClickException`, `BadParameter`, `UsageError`
   - Test exception handling in command validation and execution
   - Test error message formatting and localization
   - Test exception propagation through command groups
   - Test custom exception handling and user-defined errors

3. **Test file I/O and data processing:**
   - Analyze `examples/imagepipe/imagepipe.py` file processing workflow
   - Create tests for file argument validation and path resolution
   - Test file existence checks and permission handling
   - Test stdin/stdout redirection and piping scenarios
   - Test file format validation and content processing
   - Test large file handling and streaming operations

4. **Test terminal UI interactions:**
   - Examine `examples/termui/termui.py` UI component implementations
   - Create tests for prompt functionality with various input types
   - Test confirmation dialogs and yes/no interactions
   - Test progress bar rendering and updates
   - Test color output formatting and terminal capability detection
   - Test interactive input validation and error recovery

5. **Test edge cases and boundary conditions:**
   - Create tests with extremely long command arguments (>1000 chars)
   - Test special characters, Unicode, and escape sequences
   - Test missing file scenarios and permission denied errors
   - Test concurrent command execution and resource contention
   - Test memory limits and large dataset processing
   - Test network timeout and external dependency failures

6. **Create integration test scenarios:**
   - Design end-to-end workflows using multiple examples
   - Test realistic user journeys from examples/ directory
   - Create scenario tests combining multiple CLI features
   - Test configuration file loading and environment variable integration
   - Test plugin system and extension loading scenarios
   - Validate complete application lifecycle from init to cleanup

## Workflow
1. Execute sub-tasks.
2. Verify: run `uv run --locked pytest -q tests/opencode/test_scenarios.py`, `uv run --locked tox run -e style`. Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(scenarios): implement advanced CLI interaction tests [protocol-0001/04]"`. Push.
5. Report to user using the step report format above.