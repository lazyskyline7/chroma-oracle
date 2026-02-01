"""Shared logic for solving puzzles with unknown ("?") color slots.

This module provides core functions for handling puzzles where some positions
contain unknown/placeholder values that need to be determined through
permutation testing.
"""

import copy
import itertools
import json

from chroma_oracle.lib.collection import ContainerCollection
from chroma_oracle.lib.colour import Colour
from chroma_oracle.lib.move import Move
from chroma_oracle.lib.search import bfs, dfs


class UnknownPuzzleData:
    """Parsed data from a puzzle containing unknowns."""

    def __init__(self, raw_grid: list[list[str]]):
        self.raw_grid = raw_grid
        self.all_items = []
        self.unknown_indices = []

        for r, row in enumerate(raw_grid):
            for c, item in enumerate(row):
                if item == "UNKNOWN" or item == "?":
                    self.unknown_indices.append((r, c))
                else:
                    self.all_items.append(item)


def load_puzzle_with_unknowns(puzzle_path: str) -> UnknownPuzzleData:
    """Load a puzzle JSON file and identify unknown positions."""
    with open(puzzle_path, encoding="utf-8") as f:
        raw_grid = json.load(f)
    return UnknownPuzzleData(raw_grid)


def calculate_needed_colors(data: UnknownPuzzleData) -> list[str] | None:
    """Calculate which colors are needed to complete sets of 4.

    Returns:
        List of colors needed, or None if puzzle structure is invalid.
    """
    counts: dict[str, int] = {}
    valid_colors = [c.name for c in Colour if c.name != "UNKNOWN"]

    for item in data.all_items:
        counts[item] = counts.get(item, 0) + 1

    needed = []
    for color, c_count in counts.items():
        if c_count < 4:
            needed.extend([color] * (4 - c_count))
        elif c_count > 4:
            print(f"Error: Color {color} appears {c_count} times (more than 4).")
            return None

    missing_slots = len(data.unknown_indices) - len(needed)

    if missing_slots > 0:
        if missing_slots % 4 == 0:
            num_new_colors = missing_slots // 4
            unused_colors = [c for c in valid_colors if c not in counts]
            if len(unused_colors) >= num_new_colors:
                for i in range(num_new_colors):
                    needed.extend([unused_colors[i]] * 4)
                print(
                    f"Assumed {num_new_colors} fully hidden colors: "
                    f"{needed[-missing_slots:]}"
                )
            else:
                print(
                    f"Error: Need {num_new_colors} new colors but only "
                    f"have {len(unused_colors)} unused valid colors."
                )
                return None
        else:
            print(
                f"Error: {missing_slots} unknown slots remaining, which "
                "is not a multiple of 4. Cannot form complete sets."
            )
            return None
    elif missing_slots < 0:
        print(
            f"Error: Have {len(data.unknown_indices)} slots but existing "
            f"colors need {len(needed)} items to complete."
        )
        return None

    return needed


def generate_candidate_grids(
    data: UnknownPuzzleData, needed: list[str]
) -> list[list[list[str]]]:
    """Generate all unique permutations of candidate grids."""
    unique_perms = sorted(set(itertools.permutations(needed)))

    candidate_grids = []
    for perm in unique_perms:
        candidate_grid = copy.deepcopy(data.raw_grid)
        for idx, (r, c) in enumerate(data.unknown_indices):
            candidate_grid[r][c] = perm[idx]
        candidate_grids.append(candidate_grid)

    return candidate_grids


def solve_all_candidates(
    candidate_grids: list[list[list[str]]], algorithm: str = "BFS"
) -> list[tuple[list[list[str]], tuple[Move, ...]]]:
    """Solve all candidate grids and return successful solutions.

    Returns:
        List of (grid, moves) tuples for each solvable configuration.
    """
    solutions = []

    for candidate_grid in candidate_grids:
        try:
            collection = ContainerCollection(candidate_grid)

            result = bfs(collection) if algorithm == "BFS" else dfs(collection)

            if result:
                solutions.append((candidate_grid, result.moves))

        except (ValueError, TypeError, AttributeError, KeyError, IndexError):
            pass

    return solutions


def identify_hidden_items(
    raw_grid: list[list[str]], resolved_grid: list[list[str]]
) -> list[str]:
    """Compare raw grid with resolved grid to identify hidden items.

    Args:
        raw_grid: Original grid with "UNKNOWN" or "?" items.
        resolved_grid: Grid with actual colors filled in.

    Returns:
        List of description strings (e.g., "Container 0, Item 1: RED").
    """
    identifications = []
    for r, (row_raw, row_res) in enumerate(zip(raw_grid, resolved_grid, strict=True)):
        for c, (item_raw, item_res) in enumerate(zip(row_raw, row_res, strict=True)):
            if item_raw in ("?", "UNKNOWN"):
                identifications.append(f"Container {r}, position {c}: {item_res}")
    return identifications
