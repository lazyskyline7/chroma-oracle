from chroma_oracle.cli.printing import print_moves
from chroma_oracle.lib.collection import ContainerCollection
from chroma_oracle.lib.move import Move


def test_print_moves_captures_lines(capsys):
    moves = [Move(0, 1), Move(2, 3)]
    print_moves(moves)
    captured = capsys.readouterr()
    assert "1. Container 0 -> 1" in captured.out
    assert "2. Container 2 -> 3" in captured.out


def test_changed_annotation_detected():
    # initial collection: container 0 has one item, container 1 empty
    start = ContainerCollection(
        [["RED", "RED", "RED", "?"], ["?", "?", "?", "?"], [], []]
    )
    # perform a valid move from container 0 to container 3 (where there is space)
    move = Move(0, 3)
    after = start.after(move)

    orig_lines = str(start).splitlines()
    sim_lines = str(after).splitlines()

    annotated = []
    for i, line in enumerate(sim_lines):
        if i < len(orig_lines) and line != orig_lines[i]:
            annotated.append(line + " (changed)")
        else:
            annotated.append(line)

    # Ensure at least one container line was annotated as changed
    assert any(line.endswith(" (changed)") for line in annotated)
