# AGENTS.md - Developer Guide for Agents

This document provides instructions for AI agents working on the ChromaOracle codebase.

## 1. Project Overview
ChromaOracle is a Python-based CLI tool for solving color sorting puzzles (e.g., Ball Sort, Water Sort). It includes:
- **Algorithms**: BFS (optimal) and DFS (fast).
- **Mystery Solver**: Handling hidden state ("?") via simulation.
- **Infrastructure**: Dockerized, uses `uv` for dependency management.

## 2. Environment & Build

- **Python Version**: 3.13+
- **Dependency Manager**: [uv](https://github.com/astral-sh/uv)
- **Root Directory**: Project root contains `pyproject.toml` and `uv.lock`.

### CLI Commands
Always use `uv run` to execute commands in the environment.

- **Main Entry Point**: `uv run chroma-oracle`
- **Solving a Level**:
  ```bash
  uv run chroma-oracle solve levels/level1.json -a BFS
  ```
- **Finding Guaranteed Moves (Mystery Puzzles)**:
  ```bash
  uv run chroma-oracle strategy levels/mystery.json
  ```
- **Interactive Strategy Session**:
  ```bash
  uv run chroma-oracle strategy -i levels/mystery.json
  ```

### Development Commands
- **Install/Sync Dependencies**: `uv sync`
- **Lint (Auto-fix)**: `uv run ruff check --fix .`
- **Format**: `uv run ruff format .`
- **Type Check**: `uv run mypy chroma_oracle`
- **Run All Checks**: `uv run ruff check . && uv run ruff format --check . && uv run mypy chroma_oracle`

## 3. Testing
Tests are located in `tests/` and use `pytest`.

- **Run All Tests**: `uv run pytest`
- **Run Single Test File**: `uv run pytest tests/lib/test_search.py`
- **Run Single Test Case**: `uv run pytest tests/lib/test_search.py::test_bfs_solution`

**Testing Guidelines**:
- Write unit tests for new logic in `tests/`.
- Ensure new tests pass `mypy` (typed tests preferred).
- Use `pytest` fixtures where appropriate.

## 4. Code Style & Conventions

We strictly follow the configuration in `pyproject.toml`.

### Formatting (Ruff)
- **Line Length**: 88 characters.
- **Quotes**: Double quotes (`"`).
- **Indentation**: 4 spaces.
- **Imports**: Sorted by `isort` (part of Ruff). `chroma_oracle` is the known first-party package.

### Type Hints (MyPy)
- **Strictness**: `check_untyped_defs = true`.
- **Requirement**: All function signatures must have type annotations.
- **Generics**: Use standard collection types (`list[str]`, `dict[str, int]`) over `typing` aliases where possible (Python 3.9+ style).

### Naming
- **Functions/Variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_CASE`
- **Files**: `snake_case.py`

### Error Handling
- Use specific exceptions.
- CLI errors should use `click.ClickException` or print user-friendly messages rather than raw stack traces when appropriate.

## 5. Project Structure

- `chroma_oracle/`: Main source code.
  - `cli/`: CLI command definitions (using `click`).
  - `lib/`: Core logic (state management, algorithms).
- `tests/`: Pytest test suite.
- `levels/`: Puzzle input files (JSON).
  - Format: `[["COLOR", ...], ["COLOR", ...]]` (Bottom-to-Top).
  - Use `?` or `UNKNOWN` for hidden items in mystery puzzles.

## 6. Implementation Notes
- **Algorithms**: If modifying BFS/DFS, ensure state immutability or careful copying to avoid side effects.
- **Input Parsing**: Colors are case-sensitive strings (usually UPPERCASE). "UNKNOWN" or "?" denotes hidden items.
- **Git**: Commit messages should be descriptive (e.g., "feat: add heuristic to DFS").

---
**Note**: If you encounter `uv` command errors, verify `uv` is installed or fallback to standard `python -m pip` if necessary, but `uv` is strongly preferred.
