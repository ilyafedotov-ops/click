# Step 5: Opencode integration

## Briefing
- **Goal:** Integrate with glm-4.6 model for intelligent testing and test generation
- **Key files:**
  - `tests/opencode/opencode_client.py`
  - `tests/opencode/test_intelligent.py`
  - `tests/opencode/helpers/test_generator.py`
- **Additional info:** Leverage glm-4.6 for intelligent test case generation and validation

## Sub-tasks
1. **Complete glm-4.6 integration:**
   - Finalize `tests/opencode/opencode_client.py` with full API integration
   - Add retry logic and error handling for API calls
   - Implement response caching and rate limiting
   - Create API client configuration management
   - Add authentication and security measures
   - Implement connection pooling and timeout handling

2. **Implement intelligent test generation:**
   - Create `tests/opencode/helpers/test_generator.py`
   - Use glm-4.6 to generate test scenarios based on CLI analysis
   - Implement dynamic test case creation and validation
   - Add test scenario classification and prioritization
   - Create test data generation utilities
   - Implement test template system for reusable patterns

3. **Create intelligent validation tests:**
   - Create `tests/opencode/test_intelligent.py`
   - Test glm-4.6's ability to understand CLI behavior
   - Validate generated test cases for correctness and coverage
   - Add regression testing for generated tests
   - Implement test result validation and assertion generation
   - Create test execution monitoring and logging

4. **Add test reporting and analytics:**
   - Implement test result analysis and reporting
   - Add coverage analysis for CLI features
   - Create test execution metrics and performance tracking
   - Build test execution dashboard and visualization
   - Add test failure analysis and root cause identification
   - Implement test trend analysis and historical reporting

5. **Create integration documentation:**
   - Document the opencode integration architecture
   - Create usage examples and best practices
   - Save in `.protocols/0001-click-opencode/integration_guide.md`
   - Add API reference documentation
   - Create troubleshooting guide and FAQ
   - Document configuration options and environment setup

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(integration): complete glm-4.6 opencode integration [protocol-0001/05]"`. Push.
5. Report to user using the step report format above.