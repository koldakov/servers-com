from typing import Any, Self


class Node:
    def __init__(
        self,
        next_: Self | None,
        /,
        *,
        data: Any | None = None,
    ) -> None:
        self._next: Self | None = next_
        self.data: Any | None = data

    @property
    def next(self) -> Self | None:
        return self._next

    @next.setter
    def next(self, node: Self, /) -> None:
        if node == self:
            raise ValueError("Next node can't be the same node as itself") from None

        self._next = node


class Graph:
    def __init__(
        self,
        nodes: list[Node],
        /,
    ) -> None:
        self.nodes: list[Node] = nodes
