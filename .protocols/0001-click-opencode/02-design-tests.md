# Step 2: Design test framework

## Briefing
- **Goal:** Design opencode integration structure and test patterns for CLI testing
- **Key files:**
  - `tests/conftest.py`
  - `tests/test_testing.py`
  - `src/click/testing.py`
  - `examples/` (various CLI examples)
- **Additional info:** Design tests that can be executed by opencode glm-4.6 model

## Sub-tasks
1. **Examine existing test infrastructure:**
   - Read `tests/conftest.py` for test fixtures and configuration
   - Study `tests/test_testing.py` for click's testing utilities
   - Review `src/click/testing.py` for ClickRunner and test helpers
   - Analyze existing test patterns in `tests/test_basic.py` and `tests/test_commands.py`
   - Examine CLI examples in `examples/` directory for test scenarios
2. **Design opencode test structure:**
   - Create `tests/opencode/` directory structure with subdirectories:
     - `tests/opencode/fixtures/` for test data and sample commands
     - `tests/opencode/helpers/` for opencode-specific utilities
     - `tests/opencode/unit/` for individual command tests
   - Design test fixtures for CLI command execution using ClickRunner
   - Plan test data organization for sample commands and expected outputs
   - Create configuration for opencode glm-4.6 integration
3. **Define test categories and patterns:**
   - Basic command execution tests (simple commands, help output)
   - Argument parsing and validation tests (required/optional args, types)
   - Option handling tests (flags, parameters, defaults)
   - Multi-command CLI interaction tests (groups, subcommands, chaining)
   - Error handling and edge case tests (invalid input, missing args)
   - Terminal UI interaction tests (prompts, confirmations, progress bars)
4. **Create test framework foundation:**
   - Set up `tests/opencode/conftest.py` with opencode-specific fixtures:
     - CLI runner fixture using ClickRunner
     - Sample command fixtures from examples/
     - Test data fixtures for various scenarios
   - Create helper utilities in `tests/opencode/helpers/`:
     - Command execution helpers
     - Output assertion helpers
     - Error scenario helpers
   - Design test data structure in `tests/opencode/fixtures/`:
     - Sample command definitions
     - Expected output templates
     - Test scenario configurations
5. **Document test design decisions:**
   - Record architectural choices for test framework in `tests/opencode/README.md`
   - Document integration points with opencode glm-4.6 model
   - Specify test execution patterns and reporting format
   - Define test naming conventions and organization principles
   - Create guidelines for writing opencode-compatible tests

## Workflow
1. Execute sub-tasks.
2. Verify: run `uv run --locked pytest -q tests/`, `uv run --locked tox run -e style`. Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(design): create opencode test framework structure [protocol-0001/02]"`. Push.
5. Report to user using the step report format above.