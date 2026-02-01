# ChromaOracle 🔮

A powerful CLI tool to solve colour sorting puzzle games (like Ball Sort Puzzle, Water Sort Puzzle) using Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms.

It features a unique **Mystery Guesser** to crack levels with hidden "unseen" blocks 🕵️‍♀️.

This project is modernized to use **Python 3.13+** and **uv** for blazing fast dependency management, and includes full **Docker** support.

## ✨ Features

- **Optimal Solving:** Uses BFS to find the shortest possible path to victory.
- **Fast Search:** Uses DFS to find _any_ solution quickly for complex levels.
- **Mystery Solver:** Can deduce hidden colors (marked as `?` or `UNKNOWN`) by simulating all valid permutations.
- **Dockerized:** Run anywhere without installing Python locally.

## 🚀 Installation

### Option A: Docker (Recommended)

No need to install Python or dependencies!

1.  **Build the image:**
    ```bash
    docker build -t chroma-oracle .
    ```

You can run the image in a way that any files the container writes are persisted
to your current working directory (so `levels/..._solved` appears on the host).
Use the provided wrapper script:

```
./scripts/docker-run.sh chroma-oracle guess levels/level9.json DFS
```

This mounts `$(pwd)` into the container at `/app` and runs the command so
outputs are written to your host tree by default.

### Option B: Local Development

Requires [uv](https://github.com/astral-sh/uv).

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/lazyskyline7/chroma-oracle.git
    cd chroma-oracle
    ```

2.  **Sync Dependencies:**
    ```bash
    uv sync
    ```

## 🛠️ Usage

### 1. Standard Solver 🧩

Solve a level where all colors are known.

**Docker:**

```bash
docker run --rm chroma-oracle levels/simple_shows_differences.json
```

**Local (console script):**

```bash
uv run chroma-oracle levels/simple_shows_differences.json
```

**Options:**

- `-a, --algorithm [BFS|DFS]`: Choose algorithm (Default: BFS).
- `--verbose`: Enable debug logging.

### 2. Mystery Guesser 🕵️‍♂️

Crack levels with hidden blocks (`UNKNOWN` or `?` in the JSON file).

**Docker:**

```bash
# Finds guaranteed safe moves or solves if unique solution exists
docker run --rm chroma-oracle strategy levels/mystery.json
```

**Local (console script):**

```bash
uv run chroma-oracle strategy levels/mystery.json
```

**Interactive Mode (Recommended):**

```bash
uv run chroma-oracle strategy -i levels/mystery.json
```

_This tool analyzes all possible hidden colors. If a unique solution is found, it solves the puzzle immediately. If not, it suggests guaranteed safe moves to reveal more clues._

## 📄 Input Format

Levels are defined in JSON files as a list of lists.

- **Order:** Items are listed from **BOTTOM to TOP**.
- **Colors:** Must match valid color names.

**Example `level.json`:**

```json
[
  ["RED", "BLUE", "GREEN", "RED"], // Container 1: Red at bottom
  ["BLUE", "RED", "GREEN", "UNKNOWN"], // Container 2: Top item hidden
  [], // Empty Container
  [] // Empty Container
]
```

**Supported Colors:**
`RED`, `PINK`, `BROWN`, `GREEN`, `LIGHT_GREEN`, `DARK_GREEN`, `YELLOW`, `BLUE`, `LIGHT_BLUE`, `DARK_BLUE`, `GREY` (use for White), `PURPLE`, `ORANGE`.

## 🧠 Algorithms

### Breadth-First Search (BFS)

The BFS algorithm is designed to find the **optimal solution** (fewest moves).

- **How it works:** It evaluates the starting pattern to find all possible moves, creating a "queue" of next patterns. It then evaluates each pattern layer by layer.
- **Trade-off:** This guarantees the shortest path but can be slower and memory-intensive for very deep puzzles.

### Depth-First Search (DFS)

The DFS algorithm prioritizes **speed**.

- **How it works:** It explores a single path of moves as far as possible (down the tree) before backtracking if it hits a dead end.
- **Trade-off:** It finds _a_ solution much faster than BFS, but the solution is often not the shortest (e.g., it might take 50 moves to do what BFS does in 20).

## 🧪 Development

### Running Tests

```bash
uv run pytest
```

### Code Quality

**Lint and auto-fix with Ruff:**

```bash
uv run ruff check --fix .
```

**Format code with Ruff:**

```bash
uv run ruff format .
```

**Type check with MyPy:**

```bash
uv run mypy chroma_oracle
```

**Run all quality checks:**

```bash
uv run ruff check . && uv run ruff format --check . && uv run mypy chroma_oracle
```

### Dependency Management

**Add a runtime dependency:**

```bash
uv add <package-name>
```

**Add a development dependency:**

```bash
uv add --dev <package-name>
```

**Update all dependencies:**

```bash
uv lock --upgrade
uv sync
```

All dependencies are defined in `pyproject.toml` and locked in 
`uv.lock`. The old `requirements/` directory has been removed in 
favor of modern PEP 735 dependency groups.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
