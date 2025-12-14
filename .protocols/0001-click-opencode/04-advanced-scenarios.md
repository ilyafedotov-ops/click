# Step 4: Advanced scenarios

## Briefing
- **Goal:** Add complex CLI interaction tests covering advanced Click features
- **Key files:**
  - `tests/opencode/unit/test_advanced.py`
  - `tests/opencode/unit/test_groups.py`
  - `tests/opencode/unit/test_scenarios.py`
- **Additional info:** Focus on command groups, chains, contexts, and complex user interactions

## Sub-tasks
1. **Test command groups and hierarchies:**
   - Create `tests/opencode/unit/test_groups.py`
   - Implement nested command group structure tests
   - Test group-level options inheritance and propagation
   - Test subcommand discovery and help generation
   - Test context passing between parent and child commands
   - Validate group-level error handling and validation

2. **Implement command chaining tests:**
   - Create command chaining test infrastructure in `tests/opencode/unit/test_advanced.py`
   - Test Click's `invoke` and `pass_context` for chained commands
   - Test multi-command workflows with state sharing
   - Validate parameter passing between chained commands
   - Test error propagation in command chains
   - Implement rollback scenarios for failed chains

3. **Test advanced Click features:**
   - Test context management with `click.Context` objects
   - Test custom parameter types and validation logic
   - Test shell completion generation and integration
   - Test environment variable handling and precedence
   - Test configuration file loading and merging
   - Test custom help formatting and documentation

4. **Create scenario-based tests:**
   - Create `tests/opencode/unit/test_scenarios.py`
   - Implement realistic CLI workflow scenarios (e.g., deployment pipelines)
   - Test interactive prompts and user input handling
   - Test progress bars and long-running operations
   - Test error recovery and graceful degradation
   - Test CLI output formatting and redirection
   - Validate cross-platform compatibility scenarios

5. **Add performance and stress tests:**
   - Test CLI performance with large argument lists and inputs
   - Test memory usage during long-running operations
   - Test concurrent command execution and thread safety
   - Test resource cleanup and file handle management
   - Test CLI startup time and initialization overhead
   - Validate performance regression detection

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(tests): add advanced CLI scenario tests [protocol-0001/04]"`. Push.
5. Report to user using the step report format above.