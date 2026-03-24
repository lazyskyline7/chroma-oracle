"""Implementation of search algorithms."""

import logging
from dataclasses import dataclass

from chroma_oracle.lib.collection import ContainerCollection
from chroma_oracle.lib.move import Move


@dataclass
class Option:
    """Represents an option in the graph of possible games."""

    collection: ContainerCollection
    moves: tuple[Move, ...]


@dataclass
class BfsNode:
    """Represents a node in the BFS search tree."""

    collection: ContainerCollection
    move: Move | None
    parent: BfsNode | None
    prev_move: Move | None = None
    prev_prev_move: Move | None = None


def reconstruct_path(node: BfsNode) -> tuple[Move, ...]:
    """Reconstruct the path of moves from root to node."""
    moves = []
    current: BfsNode | None = node
    while current and current.move:
        moves.append(current.move)
        current = current.parent
    return tuple(reversed(moves))


def bfs(root: ContainerCollection) -> Option | None:
    """Perform a Breadth-first search to find an optimal solution."""
    # Ensure the search is required
    if root.is_solved:
        return Option(root, ())

    root_node = BfsNode(root, None, None)
    queue: list[BfsNode] = []
    visited: set[ContainerCollection] = {root}

    for move in root.get_moves():
        next_coll = root.after(move)
        if next_coll.is_solved:
            return Option(next_coll, (move,))
        if next_coll not in visited:
            visited.add(next_coll)
            queue.append(BfsNode(next_coll, move, root_node, move, None))

    while len(queue) > 0:
        logging.debug("Options %d", len(queue))
        next_queue: list[BfsNode] = []
        for node in queue:
            for move in node.collection.get_moves():
                # Detect trivial loops: A→B then B→A then A→B again
                if (
                    node.prev_move is not None
                    and node.prev_prev_move is not None
                    and node.prev_move == move.reverse()
                    and node.prev_prev_move == move
                ):
                    continue

                _next: ContainerCollection = node.collection.after(move)

                # Performance: Check visited before expensive state analysis
                if _next in visited:
                    continue

                is_solved = _next.is_solved
                # Skip dead-end states (no moves and not solved)
                if not is_solved and not _next.get_moves():
                    continue

                child_node = BfsNode(
                    _next,
                    move,
                    node,
                    prev_move=move,
                    prev_prev_move=node.prev_move,
                )

                # Check if a solution was found
                if is_solved:
                    return Option(_next, reconstruct_path(child_node))

                visited.add(_next)
                next_queue.append(child_node)
        queue = next_queue

    # No valid options
    return None


def dfs(root: ContainerCollection) -> Option | None:
    """Perform a depth-first search to find a solution."""
    # Ensure the search is required
    if root.is_solved:
        return Option(root, ())

    visited: set[ContainerCollection] = set()
    # Call the recursive function
    return _dfs(visited, Option(root, ()))


def _dfs(visited: set[ContainerCollection], option: Option) -> Option | None:
    col = option.collection
    if col in visited:
        return None
    visited.add(col)
    if col.is_solved:
        return option

    for move in col.get_moves():
        next_moves = list(option.moves)
        next_moves.append(move)
        next_option = Option(col.after(move), tuple(next_moves))
        result = _dfs(visited, next_option)
        if result is not None:
            return result

    # After visiting all possible moves, nothing had a solution
    return None
