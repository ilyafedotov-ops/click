# 0006 — workflow-eval-click-1765525532

## ADR-style Summary:
- **Context**: Need to run an end-to-end evaluation for Click with a focus on code-side QA downgrade handling, ensuring workflow coverage without breaking existing behavior.
- **Problem Statement**: Implement and validate QA downgrade logic while keeping the project stable, with clear steps for changes, testing, and documentation.
- **Decision**: Use a structured protocol with incremental steps: understand current behavior, implement downgrade changes, update tests, document, and finalize.
- **Alternatives**: Ad-hoc edits without protocol; skipping dedicated testing phase; postponing documentation until later.
- **Consequences**: Provides traceable progress, minimizes regressions, and ensures reproducible steps with clear checkpoints.

---

## High-Level Plan:
This section is a **contract**; do not change during implementation.

- **[Step 0: Prepare and lock plan](./00-setup.md)**: Create and commit protocol artifacts.
- **[Step 1: Baseline and requirements](./01-baseline-and-requirements.md)**: Inspect current QA downgrade logic, tests, and requirements.
- **[Step 2: Implement QA downgrade handling](./02-implement-qa-downgrade.md)**: Apply code changes for QA downgrade behavior.
- **[Step 3: Tests and coverage](./03-tests-and-coverage.md)**: Add/update tests to cover downgrade scenarios; ensure coverage.
- **[Step 4: Docs and changelog](./04-docs-and-changelog.md)**: Update documentation/changelog as needed for the new behavior.
- **[Step 5: Finalize](./05-finalize.md)**:
  * Mark PR Ready
  * Close out work

---

## Protocol Workflow (How to execute)
Follow `High-Level Plan` and this cycle for each step.

- **PROJECT_ROOT**: /home/ilya/Documents/dev-pipeline/projects/github.com/pallets/click
- **CWD (worktree)**: /home/ilya/Documents/dev-pipeline/projects/github.com/pallets/click/worktrees/tasksgodzilla-worktree
- **Protocol folder**: /home/ilya/Documents/dev-pipeline/projects/github.com/pallets/click/worktrees/tasksgodzilla-worktree/.protocols/0006-workflow-eval-click-1765525532

All work happens in the worktree (CWD).

### A. Before a new step (restore context)
1. Read `Current Step` from `context.md`.
2. Open the step file (e.g., `01-baseline-and-requirements.md`).
3. Ensure previous changes are committed.

### B. During the step (execute)
1. Do the sub-tasks in the step file.
2. Do **not** change plan files (`plan.md`, `XX-*.md`). They are the contract.
3. Follow Generic Principles below.

### C. After the step (verify & fix)
1. Run checks: `typecheck`, `lint`, `test`. Fix until green.
2. Add a `log.md` entry describing what and why (include commit ID).
3. Rewrite `context.md` for the next step.
4. Verify `main` has no stray files from our branch. Commit with `type(scope): subject [protocol-0006/YY]`. Push.
5. Report to the user in the format:
<report_format>
(Protocol, step):

**Done**: what/where/why (also in Log).

**Checks**: which ran (lint/typecheck/test), pass/fail, why.

**Git**: PR link; current branch; commit message; push status; main-branch cleanliness check.

**Working directory**: absolute CWD path.

**Protocol status**: where we are and what’s next.
</report_format>

---

## Generic Principles (MUST follow, shared)
- Balance & simplicity; avoid overengineering.
- No legacy; greenfield decisions allowed.
- Respect coding standards/linters/formatters/JSDoc.
- Keep docs current (Memory Bank), atomic.
- Quality tests: positive/negative/boundaries; reuse helpers.
- Detail & decomposition: plans executable without this chat.

---

## Reference Materials
- Project README and contribution guidelines.
- Existing QA/downgrade-related code and tests under `src/` and `tests/`.
- CI configuration in `.github/` for understanding checks.
