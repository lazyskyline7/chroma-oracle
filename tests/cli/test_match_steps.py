import os

from solver.match_steps import match_first_steps


def test_match_first_steps_finds_1_json(tmp_path, capsys):
    # Use the repo's levels folder as data
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    folder = os.path.join(repo_root, "levels", "level9_solved")
    reference = os.path.join(repo_root, "levels", "level9.json")

    matches = match_first_steps(folder, reference, n=2, algorithm="BFS")
    assert isinstance(matches, list)
    # Expect at least our example 1.json to be present
    assert any("1.json" in m for m in matches)
