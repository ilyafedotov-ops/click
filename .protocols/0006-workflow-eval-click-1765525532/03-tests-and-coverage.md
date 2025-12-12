(Protocol 0006, Step 03-tests-and-coverage):

**Done**: Added QA downgrade coverage in `tests/test_qa_downgrade.py` covering no-flag baseline, warning emission for valid lower targets, blank target handling, non-numeric target handling, and strict-mode failure that blocks execution; captured stderr deterministically by patching `_installed_click_version`. Updated protocol log/context for Step 3 completion.

**Checks**: `uv run pytest tests/test_qa_downgrade.py`; `uv run ruff check src tests`; `uv run mypy`; full `uv run pytest` (1325 passed, 21 skipped, 1 xfailed) — all passing.

**Git**: PR https://github.com/ilyafedotov-ops/click/pull/1; branch `0006-workflow-eval-click-1765525532`; commit `test: cover QA downgrade behavior [protocol-0006/03]` (cc2f3d3) pushed; working tree clean, no stray files on branch.

**Working directory**: /home/ilya/Documents/dev-pipeline/projects/github.com/pallets/click/worktrees/tasksgodzilla-worktree

**Protocol status**: Step 3 complete; ready to begin Step 4 (docs/changelog).
