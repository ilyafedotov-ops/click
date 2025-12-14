# Step 3: Implement core tests

## Briefing
- **Goal:** Build basic CLI command tests using examples and click modules
- **Key files:**
  - `tests/opencode/unit/test_basic_commands.py`
  - `tests/opencode/fixtures/sample_commands.py`
  - `examples/aliases/aliases.py`
  - `examples/naval/naval.py`
- **Additional info:** Focus on fundamental CLI operations that can be tested by opencode

## Sub-tasks
1. **Create test fixtures and sample commands:**
   - Implement `tests/opencode/fixtures/sample_commands.py` with basic click commands
   - Create test data in `tests/opencode/fixtures/test_data.py`
   - Set up helper utilities in `tests/opencode/helpers/`
2. **Implement basic command tests:**
   - Create `tests/opencode/unit/test_basic_commands.py` for simple command execution
   - Test command invocation with various arguments
   - Test help text and command discovery
3. **Test argument and option handling:**
   - Create `tests/opencode/unit/test_arguments.py` for argument parsing tests
   - Test required vs optional arguments
   - Test argument types and validation
4. **Test option functionality:**
   - Create `tests/opencode/unit/test_options.py` for option handling tests
   - Test flag options, value options, and default values
   - Test option validation and error cases
5. **Implement CLI integration tests:**
   - Test actual CLI examples from `examples/` directory
   - Test command-line interface execution patterns
   - Verify output formatting and error handling

## Workflow
1. Execute sub-tasks.
2. Verify: run `uv run --locked pytest -q tests/opencode/`, `uv run --locked tox run -e typing`. Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(tests): implement core CLI command tests [protocol-0001/03]"`. Push.
5. Report to user using the step report format above.