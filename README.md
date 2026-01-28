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

**Local:**

```bash
uv run python -m solver levels/simple_shows_differences.json
```

**Options:**

- `-a, --algorithm [BFS|DFS]`: Choose algorithm (Default: BFS).
- `--verbose`: Enable debug logging.

### 2. Mystery Guesser 🕵️‍♂️

Crack levels with hidden blocks (`UNKNOWN` or `?` in the JSON file).

**Docker:**

```bash
# Just add 'guess' before the file path!
docker run --rm chroma-oracle guess levels/mystery.json DFS
```

**Local:**

```bash
uv run python -m solver.guess levels/mystery.json DFS
```

_If a solution is found, it will be saved as `levels/mystery.json.solved_X.json`. You can then run the Standard Solver on this file to see the moves._

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

To run the test suite:

```bash
uv run pytest
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
