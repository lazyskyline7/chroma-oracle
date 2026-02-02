# ChromaOracle 🔮
[![Docker Pulls](https://img.shields.io/docker/pulls/lazyskyline/chroma-oracle)](https://hub.docker.com/repository/docker/lazyskyline/chroma-oracle)
[![Tests](https://github.com/lazyskyline7/chroma-oracle/actions/workflows/tests.yml/badge.svg)](https://github.com/lazyskyline7/chroma-oracle/actions/workflows/tests.yml)
[![Docker Publish](https://github.com/lazyskyline7/chroma-oracle/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/lazyskyline7/chroma-oracle/actions/workflows/docker-publish.yml)
[![ruff/mypy](https://img.shields.io/github/actions/workflow/status/lazyskyline7/chroma-oracle/tests.yml?label=ruff%2Fmypy%20checks)](https://github.com/lazyskyline7/chroma-oracle/actions/workflows/tests.yml)

CLI for solving colour sorting puzzles (Ball Sort, Water Sort, etc.) using BFS/DFS plus a mystery solver that infers hidden colours. Run it via `uv run chroma-oracle` or the Docker image below.

## Quick start

### Run from source

Requires **Python 3.13+**.

```bash
git clone https://github.com/lazyskyline7/chroma-oracle.git
cd chroma-oracle
uv sync
uv run chroma-oracle solve levels/simple_shows_differences.json
```

### Docker (alternative)

```
docker build -t chroma-oracle .
docker tag chroma-oracle:latest lazyskyline/chroma-oracle:latest
docker push lazyskyline/chroma-oracle:latest
```

Once the image is on Docker Hub you can pull it anywhere:

```
docker run --rm lazyskyline/chroma-oracle:latest levels/simple_shows_differences.json
```

Use `./scripts/docker-run.sh chroma-oracle ...` to mount your working tree into `/app` and forward any CLI arguments whenever you build locally.

## Features ✨

- **Optimal solving:** BFS finds the shortest move sequence.
- **Fast search:** DFS reaches a valid solution quickly for deeper puzzles.
- **Mystery solver:** Handles `UNKNOWN`/`?` entries by simulating every consistent fill and exposing guaranteed, safe moves.
- **Lightweight CLI:** Works via `pip`, `uv run`, or Docker with the same subcommands.
- **Interactive strategy:** Step through guaranteed moves, reveal hidden colours, and update levels iteratively.

## Usage

### Solve known puzzles 🧩

```bash
chroma-oracle solve levels/simple_shows_differences.json
```

The `solve` command prints the starting stacks, executes the chosen algorithm, and lists the solution or an explanation when no solution exists.

### Mystery solving & strategy 🕵️‍♂️

```bash
chroma-oracle strategy levels/mystery.json
chroma-oracle strategy -i levels/mystery.json
```

`strategy` computes all candidate solutions for puzzles containing hidden cells and reports any prefix shared by every candidate, i.e., guaranteed safe moves. Pass `-i` for an interactive session that applies one move at a time so you can update the level file between steps.

## Algorithms 🧠

- **Breadth-first search (BFS):** Guaranteed optimal (fewest moves) traversal of the puzzle graph.
- **Depth-first search (DFS):** Fast exploration for large puzzles where speed matters more than minimality.
- **Mystery handling:** Unknown slots are filled with every consistent colour arrangement; `find_all_solutions` and `find_common_prefix` extract the safe moves.

## CLI reference

| Flag | Description |
| --- | --- |
| `-a, --algorithm [BFS|DFS]` | Select the search strategy (default: BFS). |
| `--verbose` | Enable extra logging from BFS/DFS or strategy helpers. |
| `-i, --interactive` | (strategy only) Run an interactive session that pauses between guaranteed moves. |
| `--help` | Show the CLI help text. |

## Input format 📄

Levels are JSON files where each container is a list of colours from **bottom to top**. Unknown colours are represented as `"?"` or `"UNKNOWN"`.

```json
[
  ["RED", "BLUE", "GREEN", "RED"],
  ["BLUE", "RED", "GREEN", "UNKNOWN"],
  [],
  []
]
```

Supported colours: `RED`, `PINK`, `BROWN`, `GREEN`, `LIGHT_GREEN`, `DARK_GREEN`, `YELLOW`, `BLUE`, `LIGHT_BLUE`, `DARK_BLUE`, `GREY`, `PURPLE`, `ORANGE`.

## Docker Hub image

After pushing `lazyskyline/chroma-oracle`, the published image can be referenced directly:

```
docker pull lazyskyline/chroma-oracle:latest
docker run --rm lazyskyline/chroma-oracle:latest strategy levels/mystery.json
```

Setup automated builds by linking `github.com/lazyskyline7/chroma-oracle` to Docker Hub so that every push keeps the badge above fresh.

## Automation

- `Tests` workflow (`.github/workflows/tests.yml`) runs on pushes and pull requests targeting `main`, covering Ruff, formatting, MyPy, and Pytest checks.
- `Docker Publish` workflow (`.github/workflows/docker-publish.yml`) runs on pushes to `main`, logs into Docker Hub with `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN` secrets, and pushes `lazyskyline/chroma-oracle:latest`.

## Developer helpers 🧪

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy chroma_oracle
uv run pytest
```

Add new runtime dependencies via `uv add <package>` and dev dependencies via `uv add --dev <package>`. Update the lockfile with `uv lock --upgrade && uv sync` when you change dependencies.

## Contributing

Bug reports and pull requests are welcome. Follow the existing style: double-quoted strings, 88-column Ruff rules, and strict MyPy annotations.

## License

MIT. See `LICENSE`.
