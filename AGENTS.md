# Repository Guidelines

## Project Structure & Module Organization

TradingAgents is a Python package with a CLI front end. Core framework code lives in `tradingagents/`: `graph/` builds the LangGraph workflow, `agents/` contains analyst/research/trader/risk roles, `dataflows/` wraps market data providers, and `llm_clients/` handles model providers. The interactive terminal app is in `cli/`. Tests live in `tests/`, helper scripts in `scripts/`, and README images/static media in `assets/`.

## Build, Test, and Development Commands

Use Python 3.10+; Python 3.12 is the documented local default.

```bash
pip install -e ".[dev]"        # editable install with pytest and ruff
uv run --extra dev pytest      # run the full local test suite
uv run ruff check .            # lint the repository
uv run tradingagents analyze   # launch the interactive CLI
uv run python main.py          # run the package usage example
```

Docker users can copy `.env.example` to `.env`, add API keys, then run `docker compose run --rm tradingagents`.

## Coding Style & Naming Conventions

This project uses Ruff with a 100-character line length and Python 3.10 target. Follow existing style: 4-space indentation, type hints for public helpers, snake_case for modules/functions/variables, PascalCase for classes, and UPPER_SNAKE_CASE for constants. Keep provider-specific behavior isolated in `llm_clients/` or `dataflows/` rather than branching through agent prompts.

## Testing Guidelines

Tests use pytest and are configured in `pyproject.toml`. Name new tests `test_*.py` and keep them close to the behavior they cover, for example `tests/test_vendor_routing.py` for data-provider logic. Mark external-service tests with the existing `integration` marker and skip gracefully when API keys are absent. Run `uv run --extra dev pytest` before submitting changes.

## Commit & Pull Request Guidelines

Git history follows concise Conventional Commit-style subjects such as `fix(cli): ...`, `test(i18n): ...`, and `chore(models): ...`. Use a scoped subject when practical. Pull requests should describe the behavior change, list verification commands, link related issues, and include CLI screenshots or terminal excerpts when changing user-facing flows.

## Security & Configuration Tips

Do not commit `.env`, API keys, cache files, or generated reports. Prefer `TRADINGAGENTS_*` environment overrides over editing defaults for local experiments. Treat outputs as research artifacts, not financial advice.
