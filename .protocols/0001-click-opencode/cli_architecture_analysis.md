# Click repo structure + API map (repo-aware)

## Repo root
`/home/ilya/Documents/dev-pipeline/projects/1/click`

## Packaging
- **Config**: `pyproject.toml`
  - **Build backend**: flit (`[build-system]`, `[tool.flit.module]`)
  - **Source**: `src/` (see `[tool.ruff].src = ["src"]`)
  - **Pytest**: `tool.pytest.ini_options.testpaths = ["tests"]`
  - **Typing**: `tool.mypy.files = ["src", "tests/typing"]`

## Source layout (`src/click/`)
Key modules and what they do:
- **Public re-exports**: `src/click/__init__.py`
- **Core command model**: `src/click/core.py`
- **Decorator API**: `src/click/decorators.py`
- **Parsing**: `src/click/parser.py`
- **Types**: `src/click/types.py`
- **Testing utilities**: `src/click/testing.py` (includes `CliRunner`)
- **Shell completion**: `src/click/shell_completion.py`
- **Terminal UI**: `src/click/termui.py`, `src/click/_termui_impl.py`
- **Utilities / compatibility**: `src/click/utils.py`, `src/click/_utils.py`, `src/click/_compat.py`
- **Exceptions**: `src/click/exceptions.py`

## Tests (`tests/`)
- Shared runner fixture:
  - `tests/conftest.py` provides `runner = click.testing.CliRunner()`
- Coverage is broad and file-based (examples):
  - `tests/test_basic.py` — basic commands and option/argument behavior
  - `tests/test_options.py` — option parsing edge cases
  - `tests/test_arguments.py` — argument parsing + arity + env
  - `tests/test_commands.py` — command invocation, contexts, groups
  - `tests/test_shell_completion.py` — shell completion subsystem
  - `tests/test_termui.py` — prompts / term UI behaviors
  - `tests/test_testing.py` — CliRunner behaviors
  - `tests/test_parser.py` — internal parser behaviors

## Runnable examples (`examples/**/*.py`)
These are the repo’s practical “entrypoints” for smoke:
- `examples/naval/naval.py`
- `examples/aliases/aliases.py`
- `examples/completion/completion.py`
- `examples/validation/validation.py`
- `examples/termui/termui.py`

## CI parity
- `.github/workflows/tests.yaml` runs `uv run --locked tox run -e ...`.
