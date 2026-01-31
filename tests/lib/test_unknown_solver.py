"""Test the unknown_solver shared module."""

import json
import os
import tempfile

from solver.lib.unknown_solver import (
    calculate_needed_colors,
    generate_candidate_grids,
    load_puzzle_with_unknowns,
)


def test_load_puzzle_with_unknowns():
    """Test loading a puzzle with unknown positions."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([["?", "?", "RED", "RED"], ["BLUE", "BLUE", "BLUE", "BLUE"], []], f)
        temp_path = f.name

    try:
        data = load_puzzle_with_unknowns(temp_path)
        assert len(data.unknown_indices) == 2
        assert (0, 0) in data.unknown_indices
        assert (0, 1) in data.unknown_indices
        assert len(data.all_items) == 6
    finally:
        os.unlink(temp_path)


def test_calculate_needed_colors():
    """Test calculation of needed colors."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([["?", "?", "RED", "RED"], ["BLUE", "BLUE", "BLUE", "BLUE"], []], f)
        temp_path = f.name

    try:
        data = load_puzzle_with_unknowns(temp_path)
        needed = calculate_needed_colors(data)
        assert needed is not None
        assert len(needed) == 2
        assert needed.count("RED") == 2
    finally:
        os.unlink(temp_path)


def test_generate_candidate_grids():
    """Test candidate grid generation."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump([["?", "?", "RED", "RED"], ["BLUE", "BLUE", "BLUE", "BLUE"], []], f)
        temp_path = f.name

    try:
        data = load_puzzle_with_unknowns(temp_path)
        needed = calculate_needed_colors(data)
        assert needed is not None
        grids = generate_candidate_grids(data, needed)

        assert len(grids) > 0
        for grid in grids:
            for row in grid:
                for item in row:
                    assert item != "?"
    finally:
        os.unlink(temp_path)
