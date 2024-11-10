from random import choice
from typing import Any, ClassVar, NamedTuple, Self


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


def _connect_nodes(nodes: list[Node], /) -> None:
    for node in nodes:
        if len(nodes) > 1:
            node.next = choice([n for n in nodes if n != node])  # noqa: S311


class GraphBaseError(Exception):
    """Graph Base Error."""


class ConnectionPercentViolationError(GraphBaseError):
    """Connection Percent Violation Error."""


class NodesAmountViolationError(GraphBaseError):
    """Nodes Amount Violation Error."""


class MinMax(NamedTuple):
    min: int
    max: int


class Graph:
    connection_percent_cond: ClassVar[MinMax] = MinMax(min=0, max=100)
    nodes_amount_cond: ClassVar[MinMax] = MinMax(min=0, max=999)

    def __init__(
        self,
        nodes: list[Node],
        /,
    ) -> None:
        self.nodes: list[Node] = nodes

    @classmethod
    def random(
        cls,
        *,
        nodes_amount: int = 100,
        connection_percent: int = 80,
    ) -> Self:
        if connection_percent < cls.connection_percent_cond.min or connection_percent > cls.connection_percent_cond.max:
            raise ConnectionPercentViolationError() from None

        if nodes_amount < cls.nodes_amount_cond.min or nodes_amount > cls.nodes_amount_cond.max:
            raise NodesAmountViolationError() from None

        connected_nodes_len: int = int(nodes_amount * connection_percent / 100)

        connected_nodes: list[Node] = [Node(None) for _ in range(connected_nodes_len)]
        isolated_nodes: list[Node] = [Node(None) for _ in range(nodes_amount - connected_nodes_len)]

        _connect_nodes(connected_nodes)
        _connect_nodes(isolated_nodes)

        return cls([*connected_nodes, *isolated_nodes])
