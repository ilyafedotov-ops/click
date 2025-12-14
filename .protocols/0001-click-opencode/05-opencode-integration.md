# Step 5: Integration with opencode

## Briefing
- **Goal:** Connect tests with opencode glm-4.6 for end-to-end CLI testing
- **Key files:**
  - `tests/opencode/test_opencode_integration.py`
  - `tests/opencode/opencode_client.py`
  - `tests/opencode/test_scenarios.py`
- **Additional info:** Implement actual opencode glm-4.6 interaction patterns

## Sub-tasks
1. **Create opencode client infrastructure:**
   - Set up opencode API client configuration for glm-4.6
   - Implement authentication and session management utilities
   - Create request/response handling with proper error handling
   - Add retry logic and timeout management
   - Create client factory for test isolation

2. **Build integration test framework:**
   - Create base test classes for opencode integration
   - Implement opencode command execution test utilities
   - Build response parsing and validation helpers
   - Create mock opencode server for isolated testing
   - Add test fixtures for common opencode interactions

3. **Implement core integration tests:**
   - Test basic opencode client initialization and connection
   - Test simple command execution through opencode
   - Test response parsing and data extraction
   - Test error handling and recovery scenarios
   - Test session management and cleanup

4. **Create end-to-end CLI scenarios:**
   - Test complete click command workflows with opencode assistance
   - Test multi-step command sequences with state management
   - Test opencode-assisted command generation and validation
   - Test opencode debugging and troubleshooting workflows
   - Test complex CLI interactions with nested commands

5. **Add monitoring and reporting infrastructure:**
   - Create test execution metrics collection system
   - Implement structured logging with different verbosity levels
   - Build comprehensive test result reporting with summaries
   - Add performance monitoring and benchmarking
   - Create test coverage analysis for opencode integration

6. **Create configuration and utilities:**
   - Add opencode configuration management for test environments
   - Create test data generators for various CLI scenarios
   - Build helper utilities for test setup and teardown
   - Add environment-specific configuration handling
   - Create test isolation and cleanup utilities

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(integration): connect opencode glm-4.6 tests [protocol-0001/05]"`. Push.
5. Report to user using the step report format above.