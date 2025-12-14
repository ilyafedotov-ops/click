# Step 4: Add advanced scenarios

## Briefing
- **Goal:** Implement complex CLI interaction tests and edge cases
- **Key files:**
  - `tests/opencode/test_groups.py`
  - `tests/opencode/test_advanced.py`
  - `tests/opencode/test_integration.py`
- **Additional info:** Test sophisticated click features and real-world scenarios

## Sub-tasks
1. **Implement group and subcommand tests:**
   - Create test file structure for `tests/opencode/test_groups.py`
   - Implement basic command group creation tests
   - Add subcommand discovery and validation tests
   - Test nested command group hierarchies
   - Implement group-level option inheritance tests
   - Add dynamic group registration tests
   - Test group help text and documentation generation

2. **Create advanced feature tests:**
   - Create test file structure for `tests/opencode/test_advanced.py`
   - Implement command chaining and pipeline tests
   - Add context passing between commands tests
   - Test callback function execution and error handling
   - Implement custom parameter type validation tests
   - Add command alias and shortcut tests
   - Test conditional command execution

3. **Build integration scenarios:**
   - Create test file structure for `tests/opencode/test_integration.py`
   - Implement file I/O operation tests with various formats
   - Add shell completion generation and validation tests
   - Test terminal UI interaction and progress indicators
   - Implement error recovery and graceful degradation tests
   - Add environment variable integration tests
   - Test configuration file loading and merging

4. **Add performance and stress tests:**
   - Implement large argument list handling tests
   - Add memory usage profiling and validation
   - Create command execution time benchmark tests
   - Implement concurrent command execution tests
   - Add resource cleanup and leak detection tests
   - Test scalability with increasing command complexity

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(tests): add advanced CLI scenarios [protocol-0001/04]"`. Push.
5. Report to user using the step report format above.