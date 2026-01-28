# ChromaOracle 🔮

A powerful CLI tool to solve colour sorting puzzle games (like Ball Sort Puzzle, Water Sort Puzzle) using Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms. It includes a unique **Guesser** feature to crack levels with hidden mystery blocks.

This project is modernized to use **Python 3.14+** and **uv** for dependency management.

## 🎮 About the Game

The game involves a collection of containers filled with coloured items.
- Each container has a limited capacity (usually 4 items).
- The goal is to sort the colours so that each container holds only one colour.

**Rules:**
1. You can only move the **top-most** item.
2. You can only place an item onto a matching colour or into an empty container.
3. You cannot exceed a container's capacity.

## 🚀 Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast and reliable dependency management.

1. **Install uv** (if not already installed):
   ```bash
   # MacOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/lazyskyline7/chroma-oracle.git
   cd chroma-oracle
   ```

3. **Sync Dependencies:**
   ```bash
   uv sync
   ```

## 🛠️ Usage

### 1. Solve a Known Level
If you know the colors of all items in the puzzle, create a JSON file (see [Input Format](#input-format)) and run:

```bash
uv run python -m solver path/to/level.json
```

**Options:**
- `-a, --algorithm [BFS|DFS]`: Choose search algorithm (Default: BFS).
  - `BFS`: Finds the **shortest** solution (optimal) but uses more memory.
  - `DFS`: Finds **a** solution quickly, but it might not be the shortest.
- `--verbose`: Enable detailed logging.

**Example:**
```bash
uv run python -m solver levels/simple_shows_differences.json
```

### 2. Solve a Mystery Level (Hidden Colors)
Some levels have hidden items (denoted by `?` or `UNKNOWN`). Use the guesser tool to find a valid color configuration:

1. Create a JSON file using `"UNKNOWN"` for hidden items.
2. Run the guesser:
   ```bash
   uv run python -m solver.guess levels/mystery.json DFS
   ```
3. If a solution is found, it will be saved as `levels/mystery.json.solved_X.json`. Run the standard solver on this generated file to see the steps.

## 📄 Input Format

Levels are defined in JSON files as a list of lists.
- **Order:** Items are listed from **BOTTOM to TOP**.
- **Colors:** Must match valid color names (see below).

**Example `level.json`:**
```json
[
    ["RED", "BLUE", "GREEN", "RED"],    // Container 1: Red at bottom, Red at top
    ["BLUE", "RED", "GREEN", "BLUE"],   // Container 2
    [],                                 // Empty Container
    []                                  // Empty Container
]
```

**Supported Colors:**
`RED`, `PINK`, `BROWN`, `GREEN`, `LIGHT_GREEN`, `DARK_GREEN`, `YELLOW`, `BLUE`, `LIGHT_BLUE`, `DARK_BLUE`, `GREY` (use for White), `PURPLE`, `ORANGE`.

## 🧪 Development

To run the test suite:

```bash
uv run pytest
```

## 🧠 Algorithms

### Breadth-First Search (BFS)
Explores all neighbor nodes at the present depth prior to moving on to the nodes at the next depth level.
- **Pros:** Guarantees the shortest path (minimum moves).
- **Cons:** Slower on complex levels; high memory usage.

### Depth-First Search (DFS)
Explores as far as possible along each branch before backtracking.
- **Pros:** Very fast; low memory usage.
- **Cons:** Solution is often not optimal (e.g., 50 moves instead of 20).

## ⚠️ Disclaimer
This project is for educational purposes only and bears no affiliation with any specific game apps on the App Store or Google Play.