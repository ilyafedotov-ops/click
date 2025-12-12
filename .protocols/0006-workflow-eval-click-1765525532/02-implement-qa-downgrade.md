(Protocol 0006, step 02-implement-qa-downgrade.md):

**Done**:
- Added `_handle_qa_downgrade_notice` in `src/click/core.py` to honor `CLICK_QA_DOWNGRADE_TO`, warn once per invocation or raise when `CLICK_QA_DOWNGRADE_STRICT` is truthy, and sanity-check requested targets against the installed Click version without new deps.
- Hooked the notice into `Command.main` after completion handling; updated protocol `log.md`, `context.md`, and captured the QA quality report artifact.

**Checks**:
- `uv run ruff check src tests` (pass).
- `uv run mypy` (pass).
- `uv run pytest tests/test_basic.py -k basic` (pass; earlier attempt against missing `tests/test_core.py` reported no tests).

**Git**:
- PR https://github.com/ilyafedotov-ops/click/pull/1, branch `0006-workflow-eval-click-1765525532`.
- Commit `feat: implement QA downgrade handling [protocol-0006/02]` (150e95e) pushed; working tree clean with no stray files.

**Working directory**: `/home/ilya/Documents/dev-pipeline/projects/github.com/pallets/click/worktrees/tasksgodzilla-worktree`

**Protocol status**: Step 2 complete; next begin Step 3 (add downgrade coverage).
