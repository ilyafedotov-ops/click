# Step 01: Baseline and requirements

## Briefing
- **Goal:** Understand existing QA downgrade behavior, requirements, and affected surfaces before coding.
- **Key files:**
  - `src/` (core Click modules handling QA/version/downgrade logic)
  - `tests/` (existing downgrade/compatibility coverage)
  - `.github/` (CI signals for required checks)
- **Additional info:** Capture assumptions and open questions in `log.md`.

## Sub-tasks
1. Inventory current QA downgrade logic:
   - Locate candidate modules under `src/click/` (e.g., command resolution, version checks, downgrade guards).
   - Map entry points and data flow for downgrade decisions; note defaults and config/env flags.
   - Capture current behavior (what triggers downgrade, what is blocked/warned).
2. Review existing tests covering downgrade/version/QA behavior under `tests/`:
   - Identify suites/files that exercise downgrade logic, version compatibility, or QA handling.
   - Summarize covered scenarios; note missing cases relevant to upcoming change.
3. Extract requirements for the downgrade change:
   - From task description and observed behavior, list required inputs, expected outputs, and decision rules.
   - Enumerate edge cases (e.g., mismatched versions, absent QA data, forced downgrade flags).
4. Identify invariants and compatibility constraints to preserve:
   - Note behaviors that must not change (CLI UX, error shapes, warnings).
   - Record any public API or backward-compatibility expectations.
5. Update artifacts:
   - Add findings, assumptions, gaps, and planned test coverage to `log.md`.
   - Draft any open questions to resolve before implementation.

## Workflow
1. Execute sub-tasks.
2. Verify: no code changes required; if tooling is run, ensure it stays green.
3. Fix/record:
   - Add findings to `log.md` (requirements, assumptions, gaps).
   - Update `context.md`: set `Current Step` to `2`, `Next Action` to start Step 2.
   - Check `main` for stray files from our branch.
4. Commit: include logs/context updates if appropriate (`git commit -m "chore(protocol): record baseline for QA downgrade [protocol-0006/01]"`). Push.
5. Report to user using the step report format.
