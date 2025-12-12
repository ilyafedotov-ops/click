# Step 02: Implement QA downgrade handling

## Briefing
- **Goal:** Apply code changes to implement the required QA downgrade behavior while keeping compatibility.
- **Key files:**
  - `src/` modules implementing downgrade logic
  - Supporting utilities or configuration files if needed
- **Additional info:** Keep changes minimal and well-documented in code comments only where necessary.

## Sub-tasks
1. Re-read Step 1 notes to confirm expected downgrade behavior, inputs/outputs, default behavior, and negative cases to cover.
2. Locate the existing downgrade-related paths in `src/` (core logic plus any call sites) and decide insertion points for the new handling.
3. Implement the QA downgrade logic: apply the new conditions/branches, ensure correct outputs and fallbacks, and preserve existing defaults/compatibility.
4. Harden edge cases: validate inputs/metadata, enforce version bounds, and ensure error signaling matches requirements without changing public surface unintentionally.
5. Add or adjust configuration/flags needed to control downgrade behavior while keeping current defaults unchanged; update any wiring to propagate the flag.
6. Update concise inline docstrings/comments only where the new flow is non-obvious to future readers.
7. Run focused checks for touched areas (lint/typecheck/targeted tests) to catch immediate regressions.
8. Self-review diffs for correctness, minimal surface area, and alignment with requirements before proceeding.

## Workflow
1. Execute sub-tasks.
2. Verify: run `lint`, `typecheck`, and focused `test` if applicable to ensure no immediate regressions.
3. Fix/record:
   - Add to `log.md` a summary of code changes and rationale.
   - Update `context.md`: set `Current Step` to `3`, `Next Action` to start Step 3.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat: implement QA downgrade handling [protocol-0006/02]"`. Push.
5. Report to user using the step report format.
