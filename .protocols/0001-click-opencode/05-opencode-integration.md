# Step 5: Opencode integration

## Briefing
- **Goal:** Integrate with glm-4.6 and configure CI pipeline for automated CLI testing
- **Key files:**
  - `.github/workflows/tests.yaml`
  - `tests/opencode/opencode_client.py`
  - `tests/opencode/conftest.py`
  - `pyproject.toml`
- **Additional info:** Configure opencode glm-4.6 model integration and CI automation

## Sub-tasks
1. **Implement opencode client integration:**
   - Create `tests/opencode/opencode_client.py` with glm-4.6 API client class
   - Implement `OpencodeClient.execute_command()` method for CLI test execution
   - Add `OpencodeClient.parse_response()` for result parsing and validation
   - Create utility functions for test result formatting and error handling
2. **Configure test environment:**
   - Update `tests/opencode/conftest.py` with opencode pytest fixtures
   - Add `opencode_client` fixture for glm-4.6 client initialization
   - Create `test_context` fixture for test execution environment
   - Set up environment variable configuration for API keys and endpoints
3. **Integrate with CI pipeline:**
   - Review current `.github/workflows/tests.yaml` structure and test matrix
   - Add opencode test job to CI workflow with proper dependencies
   - Configure test artifact collection for opencode test results
   - Set up test reporting and failure notification mechanisms
4. **Create test execution scripts:**
   - Implement `tests/opencode/run_opencode_tests.py` for batch test execution
   - Create `tests/opencode/prepare_test_data.py` for test data generation
   - Add `tests/opencode/aggregate_results.py` for result collection and reporting
   - Set up test execution logging and debugging utilities
5. **Configure opencode glm-4.6 settings:**
   - Create `tests/opencode/config.py` for model configuration management
   - Implement API endpoint configuration and authentication setup
   - Add test execution parameters (timeout, retry logic, concurrency limits)
   - Create error handling and recovery mechanisms for API failures
6. **Test integration validation:**
   - Run individual opencode test cases to verify client functionality
   - Execute full test suite integration with `pytest tests/opencode/`
   - Validate CI pipeline execution with opencode tests
   - Test error scenarios: API failures, timeouts, malformed responses
   - Verify test result aggregation and reporting functionality

## Workflow
1. Execute sub-tasks.
2. Verify: run `uv run --locked pytest -q tests/opencode/`, `uv run --locked tox run -e typing`. Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(integration): configure opencode glm-4.6 and CI pipeline [protocol-0001/05]"`. Push.
5. Report to user using the step report format above.