# Step 6: Finalize

## Briefing
- **Goal:** Complete the protocol, mark PR ready, and close out work
- **Key files:**
  - `README.md` (update if needed)
  - `CHANGES.rst` (add entry)
  - `.protocols/0001-click-opencode/` (final updates)
  - All test files created in previous steps
- **Additional info:** Ensure all work is complete and properly documented

## Sub-tasks
1. **Final verification and testing:**
   - Run complete test suite: `uv run --locked pytest -q`
   - Run all quality checks: `uv run --locked tox run -e style`, `uv run --locked tox run -e typing`
   - Verify opencode integration works end-to-end
   - Check test coverage meets 85%+ target
   - Validate all CLI test scenarios pass
2. **Documentation updates:**
   - Update `README.md` with CLI testing information if applicable
   - Add entry to `CHANGES.rst` documenting the new CLI testing capabilities
   - Ensure all new test files have proper documentation
   - Review and update any inline documentation in test files
3. **Final protocol cleanup:**
   - Review and update `log.md` with final summary
   - Update `context.md` to mark protocol complete
   - Ensure all protocol files are consistent and complete
   - Verify all step files are properly formatted and complete
4. **Prepare PR for merge:**
   - Remove draft status from PR/MR
   - Update PR description with final summary
   - Ensure all CI checks pass
   - Address any remaining PR comments or feedback
5. **Final repository validation:**
   - Check that `main` branch has no stray files
   - Verify all commits follow project conventions
   - Confirm no breaking changes were introduced
   - Validate repository structure integrity
6. **Protocol completion:**
   - Mark protocol as completed in final log entry
   - Document any lessons learned or future improvements
   - Prepare handoff documentation
   - Archive protocol artifacts appropriately

## Workflow
1. Execute sub-tasks.
2. Verify: run `uv run --locked pytest -q`, `uv run --locked tox run -e style`, `uv run --locked tox run -e typing`. Fix failures.
3. Fix/record:
   - Add final entry to `log.md` with completion summary.
   - Update `context.md`: set `Current Step` to `Complete`, `Status` to `Done`.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "feat(finalize): complete CLI testing protocol implementation [protocol-0001/06]"`. Push.
5. Report to user using the step report format above, marking the protocol as complete.