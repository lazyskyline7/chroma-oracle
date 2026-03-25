"""A container is a vessle with a limited capacity that holds items."""

from __future__ import annotations

import collections.abc
from collections.abc import Sequence
from typing import Any, cast

from chroma_oracle.lib.item import Item


class Container:
    """Represents a capacity limited container in the game."""

    def __init__(
        self,
        initial_content: Sequence[Item] | Container | Sequence[str],
        capacity: int | None = None,
    ):
        """Create a container with `intial_content` and `capacity`."""
        self._capacity = capacity or 4
        # Ensure this is only ever set to the maximum size
        self.__data: tuple[Item, ...]
        self.__iter_val = 0  # Initialize iterator value

        # Lazy cache fields
        self._is_unique: bool | None = None
        self._is_solved: bool | None = None
        self._num_matching_head: int | None = None

        if isinstance(initial_content, Container):
            self._capacity = capacity or initial_content.capacity
            self.__data = initial_content.data[:capacity]
            # Inherit caches if any
            self._is_unique = initial_content._is_unique
            self._is_solved = initial_content._is_solved
            self._num_matching_head = initial_content._num_matching_head
        else:
            type_map = set(map(type, iter(initial_content)))
            if type_map == {Item}:
                initial_content = cast(
                    Sequence[Item], initial_content[: self._capacity]
                )
                self.__data = tuple(initial_content)
            elif type_map == {str}:
                initial_content = cast(Sequence[str], initial_content[: self._capacity])
                self.__data = tuple(
                    Item(value) for value in initial_content[: self._capacity]
                )
            elif type_map == set():
                self.__data = ()
            else:
                raise TypeError(
                    f"Unknown initializer: {initial_content.__class__.__name__}"
                    f": {type_map.__repr__()}"
                )

    @property
    def data(self) -> tuple[Item, ...]:
        """Non-settable public exposure of the internal data."""
        return self.__data

    @property
    def capacity(self) -> int:
        """Get the capacity of this container."""
        return self._capacity

    @property
    def is_empty(self) -> bool:
        """Check if there are any items in the container.

        Returns true if the container is empty.
        """
        return len(self.__data) == 0

    @property
    def is_full(self) -> bool:
        """Check if the container is full.

        Returns true if the container contains it's maximum number of items.
        """
        return len(self.__data) >= self.capacity

    @property
    def is_unique(self) -> bool:
        """Check if the container has a unique collection of items.

        Returns true if empty or all contents are the same colour.
        """
        if self._is_unique is not None:
            return self._is_unique
        if len(self.__data) <= 1:
            self._is_unique = True
            return True
        first = self.__data[0]
        self._is_unique = all(item == first for item in self.__data)
        return self._is_unique

    @property
    def is_solved(self) -> bool:
        """Check if the container is solved.

        Returns true if empty or full and all contents are the same colour.
        """
        if self._is_solved is not None:
            return self._is_solved
        self._is_solved = self.is_empty or (self.is_unique and self.is_full)
        return self._is_solved

    @property
    def head(self) -> Item | None:
        """Get the top most item in the container or None if empty."""
        if self.is_empty:
            return None
        return self.__data[-1]

    @property
    def num_matching_head(self) -> int:
        """Count of consecutive items that match `self.head`.

        This includes `self.head` so for a non-empty container will
        always be one and will be zero if the container is empty.
        """
        if self._num_matching_head is not None:
            return self._num_matching_head

        data_len = len(self.__data)
        if data_len == 0:
            self._num_matching_head = 0
            return 0

        count = 1
        head = self.__data[-1]
        for item in reversed(self.__data[:-1]):
            if item == head:
                count += 1
            else:
                break
        self._num_matching_head = count
        return count

    def test(self, item: Item | None) -> bool:
        """Check if `item` can be put in this container."""
        return not (self.is_full or (not self.is_empty and self.__data[-1] != item))

    def popped(self) -> tuple[Container, list[Item]]:
        """Remove as many matching head items as possible.

        Returns a tuple of (new_container, items_removed).
        """
        count = self.num_matching_head
        if count == 0:
            return self, []

        items_removed = list(self.__data[-count:])
        new_data = self.__data[:-count]
        new_container = Container(new_data, self.capacity)
        return new_container, items_removed

    def pushed(self, items: Sequence[Item]) -> Container:
        """Add items to this collection.

        Returns a new container instance.
        """
        if not items:
            return self
        if not self.test(items[0]):
            raise ValueError(f"Cannot add item {items[0]} to container {self}")

        new_data = self.__data + tuple(items)
        if len(new_data) > self.capacity:
            raise ValueError("Container capacity exceeded")

        return Container(new_data, self.capacity)

    def pour(self, target: Container) -> bool:
        """Move the head item from this container to target container.

        If there are multiple concurrent items that are equal, move as many as
        fit within `target` over to it.

        Returns a bool indicating if any items were successfully moved.
        """
        head = self.head
        if head is None:
            return False
        if not target.test(head):
            return False

        # Calculate how many can be moved
        num_to_move = min(self.num_matching_head, target.capacity - len(target))
        if num_to_move == 0:
            return False

        items_to_move = list(self.__data[-num_to_move:])

        # Mutate the existing instances for compatibility
        self.__data = self.__data[:-num_to_move]
        # We can't use target.pushed here because it creates a new instance
        # and we need to mutate the items in-place for this legacy method.
        target.__data = target.__data + tuple(items_to_move)

        # Clear caches
        self._is_unique = self._is_solved = self._num_matching_head = None
        target._is_unique = target._is_solved = target._num_matching_head = None

        return True

    def add(self, item: Item) -> bool:
        """Add `item` to this collection.

        Returns a boolean indiciating success.
        """
        if not self.test(item):
            return False

        new_self = self.pushed([item])
        self.__data = new_self.data

        # Clear cache
        self._is_unique = self._is_solved = self._num_matching_head = None

        return True

    def copy(self) -> Container:
        """Create a new container with the same data.

        The new container can be mutated using the `add` function
        without affecting the original container.
        """
        return Container(self)

    def __eq__(self, other: Any) -> bool:
        """Check if this container is equal to other."""
        if isinstance(other, Container):
            return self.__data == other.data
        if isinstance(other, collections.abc.Sequence):
            return self.__data == tuple(other)
        return False

    def __ne__(self, other: Any) -> bool:
        """Check if this container is not equal to other."""
        return not self.__eq__(other)

    def __str__(self) -> str:
        """Get the string representation of this container."""
        content = [str(content) for content in self.__data]
        padding = ""
        if len(content) < self.capacity:
            padding = " " * (self.capacity - len(self.__data))
        return f"[{''.join(content)}{padding}]"

    def __repr__(self) -> str:
        """Get a representation of the container."""
        return f"[{','.join(item.__repr__() for item in self.__data)}]"

    def __hash__(self) -> int:
        """Get the hash of this container."""
        return hash(self.__data)

    def __len__(self) -> int:
        """Return the number of items contained."""
        return len(self.__data)

    def __getitem__(self, idx: int | slice):
        """Get the `item` at `index`."""
        return self.__data[idx]

    def __iter__(self):
        """Iterate over this container's items."""
        return iter(reversed(self.__data))
