# Step 2: Design test framework

## Briefing
- **Goal:** Create opencode integration test structure for CLI testing
- **Key files:**
  - `tests/opencode/` (new directory)
  - `tests/conftest.py`
  - `pyproject.toml`
- **Additional info:** Design a test framework that integrates opencode with glm-4.6 for intelligent CLI testing

## Sub-tasks
1. **Create opencode test directory structure:**
   - Create `tests/opencode/` directory with proper Python package structure
   - Set up `tests/opencode/__init__.py` with package metadata and imports
   - Create subdirectories: `fixtures/`, `helpers/`, `unit/`, `integration/`
   - Add `__init__.py` files to each subdirectory for proper Python package structure
   - Create `.gitkeep` files in empty directories to ensure they're tracked

2. **Design opencode client integration:**
   - Create `tests/opencode/opencode_client.py` with base OpencodeClient class
   - Implement glm-4.6 API connection with proper authentication and error handling
   - Add CLI command execution wrapper with timeout and output capture
   - Implement response parsing utilities for structured CLI output analysis
   - Add retry logic and rate limiting for API calls
   - Create mock client for testing without API dependencies

3. **Create test fixtures and helpers:**
   - Design `tests/opencode/fixtures/sample_commands.py` with comprehensive test CLI commands
   - Create `tests/opencode/fixtures/test_data.py` with sample inputs and expected outputs
   - Implement `tests/opencode/helpers/assertions.py` with CLI-specific assertion helpers
   - Add `tests/opencode/helpers/cli_runner.py` for consistent CLI execution environment
   - Create `tests/opencode/helpers/test_context.py` for test context management
   - Add `tests/opencode/helpers/data_generators.py` for dynamic test data creation

4. **Set up test configuration:**
   - Update `tests/conftest.py` with opencode-specific fixtures and configuration
   - Create `tests/opencode/conftest.py` for opencode-specific pytest configuration
   - Configure pytest settings in `tests/opencode/pytest.ini` for opencode test discovery
   - Add environment configuration template in `tests/opencode/.env.test` for glm-4.6 API access
   - Update `pyproject.toml` with opencode test dependencies and configuration
   - Create test markers and categorization for different test types

5. **Create test plan document:**
   - Document the complete test framework architecture in design document
   - Define test data management strategy with fixtures and factories
   - Specify test execution patterns and CI/CD integration approach
   - Document error handling and debugging strategies for opencode tests
   - Create test coverage requirements and quality gates
   - Save comprehensive design in `.protocols/0001-click-opencode/test_framework_design.md`

## Workflow
1. Execute sub-tasks in order, ensuring each component builds upon previous work.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(design): create opencode test framework structure [protocol-0001/02]"`. Push.
5. Report to user using the step report format above.