# Work Log: 0006 — workflow-eval-click-1765525532

This is an append-only log:

- Initialized protocol artifacts and branch setup for Step 0; preparing initial commit `feat(protocol): add plan for 0006-workflow-eval-click-1765525532 [protocol-0006/00]` to lock plan files.
- Committed plan artifacts (3c2f870) and published branch `0006-workflow-eval-click-1765525532`, opened draft PR https://github.com/ilyafedotov-ops/click/pull/1.
- 2025-12-12 07:55:39 UTC - 00-setup.md executed via Codex (gpt-5.1-codex-max); QA pending.
- 2025-12-12 07:55:39 UTC - 00-setup.md QA skipped by policy.
- 2025-12-12 07:59:03 UTC - Step 1 baseline: scanned `src/click` and found no existing QA/downgrade hooks; only version-related surfaces are `Command.main`/`Context` flow, `decorators.version_option`, and `shell_completion.BashComplete._check_version` warning on old Bash. Tests have no downgrade coverage (only typing stub for `version_option` and completion fixture patch). Working requirements for the new behavior: opt-in env flag `CLICK_QA_DOWNGRADE_TO` to signal a QA-requested fallback target; default is no effect, warn about downgrade by default, allow a strict failure switch if needed, avoid new dependencies, and print at most once per invocation even if metadata is absent/invalid. Invariants to keep: existing CLI UX and version output unchanged when flag is unset; no auto-downgrade side effects. Planned tests (Step 3): no-flag baseline, warning emission when downgrade requested, strict/abort mode, invalid/blank env handling, and ensuring other commands still execute.
