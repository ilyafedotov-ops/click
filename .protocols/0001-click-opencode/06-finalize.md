# Step 6: Finalize

## Briefing
- **Goal:** Complete the E2E CLI test implementation and prepare for release
- **Key files:**
  - `README.md` (update with test documentation)
  - `pyproject.toml` (if dependencies needed)
  - `.github/workflows/` (CI configuration)
- **Additional info:** Ensure all tests pass and documentation is complete

## Sub-tasks
1. **Complete test coverage:**
   - Run full test suite using `pytest tests/` and ensure all pass
   - Check test coverage metrics using `pytest --cov=src/click`
   - Fix any failing tests by examining error logs and updating test assertions
   - Validate opencode integration functionality by running integration tests specifically
   - Ensure edge cases and error scenarios are properly covered

2. **Update documentation:**
   - Add comprehensive test documentation section to README.md with setup instructions
   - Create test execution guide in docs/testing.md with examples and troubleshooting
   - Document opencode integration setup in docs/opencode-integration.md
   - Update API documentation in docs/api.md to reflect any new testing utilities
   - Add examples of E2E test usage in examples/ directory

3. **Configure CI/CD:**
   - Review and update existing test workflows in `.github/workflows/tests.yaml`
   - Add opencode-specific testing configuration to CI pipeline
   - Configure automated test reporting with coverage badges
   - Set up environment variables for opencode integration in GitHub Actions secrets
   - Ensure matrix testing covers multiple Python versions

4. **Final validation:**
   - Run complete linting using pre-commit hooks: `pre-commit run --all-files`
   - Perform type checking: `mypy src/click/` or equivalent typecheck command
   - Execute final test suite: `pytest tests/ -v --cov=src/click --cov-report=html`
   - Validate all documentation links and formatting using `mkdocs build` or equivalent
   - Prepare release notes summarizing new E2E testing capabilities
   - Verify no breaking changes were introduced

## Workflow
1. Execute sub-tasks in order.
2. Verify: run `lint`, `typecheck`, `test` commands. Fix any failures before proceeding.
3. Fix/record:
   - Add detailed entry to `log.md` documenting what was done and why (including non-obvious decisions).
   - Update `context.md`: increment `Current Step` to 6, set `Next Action` to "Protocol Complete".
   - Check `main` branch for any stray files from our branch using `git diff main...HEAD`.
4. Commit: `git add .` then `git commit -m "feat(finalize): complete E2E CLI test implementation [protocol-0001/06]"`. Push to remote.
5. Report to user using the step report format specified in plan.md.

## Final Actions
- Mark PR as Ready for Review (remove Draft status in GitHub)
- Request review from project maintainers
- Update protocol status to Completed in context.md
- Archive protocol documentation by moving to `.protocols/archive/0001-click-opencode/`
- Create summary of protocol achievements for future reference