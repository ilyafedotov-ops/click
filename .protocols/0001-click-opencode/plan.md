# 0001 — click-opencode

## ADR-style Summary:
- **Context**: Need to create comprehensive end-to-end CLI tests for the Click library using opencode with glm-4.6 model
- **Problem Statement**: Current test coverage may not adequately test CLI functionality from a user perspective; need automated CLI testing that mimics real user interactions
- **Decision**: Implement E2E CLI tests using opencode framework with glm-4.6 model to test Click's command-line interface comprehensively
- **Alternatives**: Manual CLI testing, unit tests only, other automation frameworks
- **Consequences**: Increased test coverage, better CLI reliability, additional test maintenance overhead

---

## High-Level Plan:
This section is a **contract**; do not change during implementation.

- **[Step 0: Prepare and lock plan](./00-setup.md)**: Create and commit protocol artifacts.
- **[Step 1: Analyze CLI architecture](./01-analyze-cli.md)**: Document Click's CLI structure and identify test scenarios.
- **[Step 2: Design test framework](./02-design-tests.md)**: Create opencode integration test structure.
- **[Step 3: Implement core tests](./03-implement-core.md)**: Build basic CLI functionality tests.
- **[Step 4: Advanced scenarios](./04-advanced-scenarios.md)**: Add complex CLI interaction tests.
- **[Step 5: Opencode integration](./05-opencode-integration.md)**: Integrate with glm-4.6 model for intelligent testing.
- **[Step 6: Finalize](./06-finalize.md)**:
  * Mark PR Ready
  * Close out work

---

## Protocol Workflow (How to execute)
Follow `High-Level Plan` and this cycle for each step.

- **PROJECT_ROOT**: /home/ilya/Documents/dev-pipeline/projects/1/click
- **CWD (worktree)**: /home/ilya/Documents/dev-pipeline/projects/1/click/worktrees/tasksgodzilla-worktree
- **Protocol folder**: /home/ilya/Documents/dev-pipeline/projects/1/click/worktrees/tasksgodzilla-worktree/.protocols/0001-click-opencode

All work happens in the worktree (CWD).

### A. Before a new step (restore context)
1. Read `Current Step` from `context.md`.
2. Open the step file (e.g., `01-analyze-cli.md`).
3. Ensure previous changes are committed.

### B. During the step (execute)
1. Do the sub-tasks in the step file.
2. Do **not** change plan files (`plan.md`, `XX-*.md`). They are the contract.
3. Follow Generic Principles below.

### C. After the step (verify & fix)
1. Run checks: `typecheck`, `lint`, `test`. Fix until green.
2. Add a `log.md` entry describing what and why (include commit ID).
3. Rewrite `context.md` for the next step.
4. Verify `main` has no stray files from our branch. Commit with `type(scope): subject [protocol-0001/YY]`. Push.
5. Report to the user in the format:
<report_format>
(Protocol, step):

**Done**: what/where/why (also in Log).

**Checks**: which ran (lint/typecheck/test), pass/fail, why.

**Git**: PR link; current branch; commit message; push status; main-branch cleanliness check.

**Working directory**: absolute CWD path.

**Protocol status**: where we are and what's next.
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
- Click documentation: docs/
- Existing tests: tests/
- Examples: examples/
- pytest configuration: pyproject.toml
