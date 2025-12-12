# Step 04: Docs and changelog

## Briefing
- **Goal:** Document the QA downgrade change appropriately (user-facing docs and changelog if required).
- **Key files:**
  - `docs/` or `README.rst/md` as applicable
  - `CHANGES.rst` or similar changelog file
- **Additional info:** Keep documentation concise and aligned with project style.

## Sub-tasks
1. Locate documentation entry points:
   - Identify where QA-related behavior is documented (e.g., `docs/`, `README.rst/md`).
   - Note style/structure used for similar feature notes.
2. Describe QA downgrade behavior:
   - Draft concise explanation of the new behavior, flags/options, and expected outcomes.
   - Add usage/example snippet if patterns exist nearby; match existing formatting.
3. Update documentation files:
   - Insert the drafted content into the appropriate doc sections with consistent headings/links.
   - Cross-check for anchor consistency and table of contents updates if needed.
4. Add changelog entry:
   - Open `CHANGES.rst` (or equivalent) and add a brief entry under the correct version/unreleased section.
   - Include compatibility notes or migration guidance if applicable.
5. Proof and align style:
   - Read updated docs/changelog for clarity, tense, and voice.
   - Ensure terminology matches existing docs conventions.
6. Validate and guard regressions:
   - Run doc-related lint/build if the project provides commands; otherwise run `lint`/`test` to ensure no regressions.
   - Address any issues uncovered.
7. Record protocol artifacts:
   - Update `log.md` with what changed and why (reference commit hash when available).
   - Ensure `context.md` will reflect step completion in Workflow updates.

## Workflow
1. Execute sub-tasks in order above.
2. Verify: run any required doc lint/build if present; otherwise ensure existing `lint`/`test` still pass.
3. Fix/record:
   - Add to `log.md` doc updates and rationale.
   - Update `context.md`: set `Current Step` to `5`, `Next Action` to start Step 5.
   - Check `main` for stray files from our branch.
4. Commit: `git add .` then `git commit -m "docs: document QA downgrade behavior [protocol-0006/04]"`. Push.
5. Report to user using the step report format.
