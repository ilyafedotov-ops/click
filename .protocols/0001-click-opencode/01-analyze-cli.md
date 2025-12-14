# Step 1: Analyze CLI architecture

## Briefing
- **Goal:** Document Click's CLI structure and identify comprehensive test scenarios
- **Key files:**
  - `src/click/core.py`
  - `src/click/decorators.py`
  - `src/click/parser.py`
  - `examples/`
  - `tests/test_basic.py`
- **Additional info:** Focus on understanding Click's command structure, option handling, and user interaction patterns

## Sub-tasks
1. **Examine core Click architecture:**
   - Read `src/click/core.py` to understand Command, Group, and Context classes
   - Analyze `src/click/decorators.py` for command and option decorators
   - Review `src/click/parser.py` for argument parsing logic
   - Document class hierarchies and key methods
   - Identify entry points and data flow

2. **Study existing examples:**
   - Review all examples in `examples/` directory
   - Document different CLI patterns (simple commands, groups, complex hierarchies)
   - Identify common use cases and edge cases
   - Extract reusable patterns for test scenarios
   - Note any advanced features demonstrated

3. **Analyze current test coverage:**
   - Review `tests/test_basic.py` and related test files
   - Identify gaps in CLI testing from user perspective
   - Document what aspects need E2E testing
   - Map existing tests to CLI features
   - Highlight missing integration scenarios

4. **Create CLI test matrix:**
   - Document all CLI scenarios to test (basic commands, options, arguments, groups, etc.)
   - Prioritize scenarios based on common usage patterns
   - Define test categories (smoke, regression, edge cases)
   - Create test data requirements matrix
   - Save analysis in `.protocols/0001-click-opencode/cli_architecture_analysis.md`

5. **Document user interaction patterns:**
   - Identify common CLI workflows (help, validation, error handling)
   - Document input/output patterns
   - Map user expectations to CLI behaviors
   - Note platform-specific considerations

6. **Validate analysis completeness:**
   - Cross-reference with Click documentation
   - Ensure all major features are covered
   - Verify test matrix aligns with project goals
   - Review analysis for gaps or inconsistencies

## Workflow
1. Execute sub-tasks in order.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` what/why (non-obvious decisions).
   - Update `context.md`: increment `Current Step`, set `Next Action`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(analysis): document CLI architecture and test scenarios [protocol-0001/01]"`. Push.
5. Report to user using the step report format above.