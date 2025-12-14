# Step 6: Finalize

## Briefing
- **Goal:** Complete the E2E CLI testing implementation and prepare for merge
- **Key files:**
  - `README.md` (update with test information)
  - `CHANGES.rst`
  - All test files in `tests/opencode/`
- **Additional info:** Ensure all tests pass, documentation is complete, and PR is ready for review

## Sub-tasks
1. **Run comprehensive test suite:**
   - Execute all opencode tests: `uv run --locked pytest tests/opencode/ -v`
   - Run full test suite to ensure no regressions: `uv run --locked pytest -q`
   - Fix any failing tests or issues
   - Verify test coverage meets 85%+ target
   - Run specific test scenarios to validate edge cases

2. **Update documentation:**
   - Update `README.md` with information about E2E CLI testing
   - Add entry to `CHANGES.rst` documenting the new testing capabilities
   - Create `tests/opencode/README.md` with usage instructions
   - Review and update any API documentation affected by changes
   - Ensure all docstrings are accurate and complete

3. **Code quality and cleanup:**
   - Run linting: `uv run --locked tox run -e style`
   - Run type checking: `uv run --locked tox run -e typing`
   - Remove any debug code or temporary files
   - Verify all imports are correctly organized
   - Check for unused dependencies or imports

4. **Final integration testing:**
   - Test the complete workflow from CLI analysis to intelligent test generation
   - Validate that glm-4.6 integration works correctly
   - Ensure all test scenarios provide meaningful coverage
   - Run end-to-end workflow tests manually
   - Verify error handling and edge cases

5. **Prepare for merge:**
   - Update PR description with final summary
   - Mark PR as ready for review
   - Update `context.md` with completion status
   - Perform final git status check
   - Ensure all changes are properly committed

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: set `Current Step` to `completed`, set final status.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(finalize): complete E2E CLI testing implementation [protocol-0001/06]"`. Push.
5. Report to user using the step report format above.