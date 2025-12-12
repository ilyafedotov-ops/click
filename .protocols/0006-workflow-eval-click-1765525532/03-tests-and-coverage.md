# Step 03: Tests and coverage

## Briefing
- **Goal:** Ensure QA downgrade behavior is fully covered with targeted tests (positive, negative, boundaries).
- **Key files:**
  - `tests/` (add/update cases for downgrade scenarios)
  - Any fixtures or helpers in `tests/` supporting the new coverage
- **Additional info:** Align with existing testing patterns; prefer minimal fixtures and reuse helpers.

## Sub-tasks
1. Identify existing downgrade-related tests and helpers in `tests/` to reuse patterns/fixtures.
2. List concrete scenarios to cover: successful downgrade, prevented/invalid downgrade, boundary inputs, backward-compatible paths.
3. Add or update test modules in `tests/` to implement these scenarios, reusing fixtures; add minimal new fixtures only if required.
4. Run targeted tests for the touched modules to verify behavior before full suite; capture failures.
5. Adjust code or tests based on failures to align with expected downgrade behavior and backward compatibility.
6. Run `lint`, `typecheck`, and full `test` (or the project’s recommended full suite) until all are green.
7. Update `log.md` with test coverage notes, scenarios added, and any deviations from the initial plan.

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, `test` (scope as needed). Fix failures.
3. Fix/record:
   - Add to `log.md` test additions and outcomes.
   - Update `context.md`: set `Current Step` to `4`, `Next Action` to start Step 4.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "test: cover QA downgrade behavior [protocol-0006/03]"`. Push.
5. Report to user using the step report format.
