# Step 05: Finalize

## Briefing
- **Goal:** Wrap up the work, ensure PR is ready, and close protocol artifacts.
- **Key files:**
  - `.protocols/0006-workflow-eval-click-1765525532/context.md`
  - `.protocols/0006-workflow-eval-click-1765525532/log.md`
  - PR description/metadata
- **Additional info:** Ensure all previous steps are committed and pushed.

## Sub-tasks
1. Open PR diff and description; verify summary, testing notes, and link to protocol are present. Mark PR status to Ready for Review.
2. Run `python -m compileall src tests` (if applicable), `tox -e lint`, `tox -e typecheck`, and `tox -e py` (or the project’s standard `lint/typecheck/test` commands). Capture pass/fail and any reruns needed.
3. If any checks fail, fix issues, rerun until green, and keep notes for `log.md`.
4. Update `.protocols/0006-workflow-eval-click-1765525532/context.md`: set `Status` to `Done`, `Current Step` to `5`, `Next Action` to "Await review/merge", and refresh any metadata (branch, PR link).
5. Add final entry to `.protocols/0006-workflow-eval-click-1765525532/log.md`: include commit hash, summary of work completed, checks run with results, and remaining risks (if any).
6. Verify cleanliness: `git status` should be clean; add/commit any remaining tracked changes with `git add` then `git commit -m "chore: finalize QA downgrade protocol [protocol-0006/05]"` if needed. Push branch to remote.
7. Confirm main branch hygiene: ensure no stray files from feature branch exist on `main` (e.g., `git checkout main && git status` or compare clean state), then return to worktree branch.
8. Prepare final user report in the required format with paths and command results.

## Workflow
1. Execute the sub-tasks in order, resolving any test/lint/typecheck failures immediately.
2. Verify all final checks (`lint`, `typecheck`, `test`) pass and PR metadata is complete.
3. Fix/record:
   - Log all outcomes in `log.md`.
   - Update `context.md` to reflect completion and waiting status.
   - Ensure `main` is clean of branch artifacts.
4. Commit/push as needed: `git add .` then `git commit -m "chore: finalize QA downgrade protocol [protocol-0006/05]"` (if new changes), followed by `git push`.
5. Report to user using the step report format and confirm readiness for review/merge.
