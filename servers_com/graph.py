from random import randint, sample
from typing import Any, ClassVar, NamedTuple, Self


class Node:
    def __init__(
        self,
        id_: int,
        /,
        *,
        data: Any | None = None,
        connections_limit: int | None = None,
    ) -> None:
        self.id: int = id_
        self.connections: list[Self] = []
        self.data: Any | None = data
        self.connections_limit: int | None = connections_limit

    def add_connection(self, node: Self, /):
        if node not in self.connections:
            self.connections.append(node)

    def __eq__(self, other: Any, /) -> bool:
        if not isinstance(other, Node):
            raise ValueError() from None

        return self.id == other.id


class GraphBaseError(Exception):
    """Graph Base Error."""


class ConnectionPercentViolationError(GraphBaseError):
    """Connection Percent Violation Error."""


class NodesAmountViolationError(GraphBaseError):
    """Nodes Amount Violation Error."""


class MinRandConnectionsViolationError(GraphBaseError):
    """Min Rand Connections Violation Error."""


class GraphConfigurationError(GraphBaseError):
    """Graph Configuration Error."""


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
        *,
        allow_loop_connections: bool = False,
        connection_percent: int = 80,
        connection_limit: int = 1,
    ) -> None:
        self.nodes: list[Node] = nodes
        self.allow_loop_connections: bool = allow_loop_connections
        self.connection_percent: int = connection_percent
        self.connection_limit: int = connection_limit

    @property
    def limited_nodes(self) -> list[Node]:
        return [n for n in self.nodes if len(n.connections) == n.connections_limit]

    @property
    def unlimited_nodes(self) -> list[Node]:
        return [n for n in self.nodes if n.connections_limit is None]

    @property
    def available_nodes(self) -> list[Node]:
        def is_node_available(node: Node, /) -> bool:
            if node.connections_limit is None:
                return True

            if node.connections_limit < len(node.connections):
                return True

            return False

        return [n for n in self.nodes if is_node_available(n)]

    def human_readable_nodes(self) -> list[tuple[int, int | None, list[int]]]:
        return [(node.id, node.connections_limit, [conn.id for conn in node.connections]) for node in self.nodes]

    def set_limits(self) -> None:
        limits_amount: int = len(self.nodes) - int(len(self.nodes) * self.connection_percent / 100)
        nodes: list[Node] = sample(self.nodes, limits_amount)
        for node in nodes:
            node.connections_limit = self.connection_limit

    def populate_limited_nodes(self) -> None:
        population: list[Node] = self.available_nodes
        for node in [n for n in self.nodes if n.connections_limit is not None]:
            if self.allow_loop_connections is False:
                population = [n for n in self.available_nodes if n != node]

            try:
                connections = sample(population, 1)
            except ValueError:
                raise GraphConfigurationError() from None

            for connection in connections:
                node.add_connection(connection)
                connection.add_connection(node)

    def populate_nodes(
        self,
        min_rand_connections: int,
        /,
    ) -> None:
        self.set_limits()
        try:
            self.populate_limited_nodes()
        except GraphConfigurationError:
            raise

        unlimited_nodes: list[Node] = [n for n in self.nodes if n.connections_limit is None]
        population: list[Node] = unlimited_nodes
        for node in unlimited_nodes:
            if self.allow_loop_connections is False:
                population = [n for n in unlimited_nodes if n != node]

            try:
                connections: list[Node] = sample(
                    population,
                    randint(2, min_rand_connections),  # noqa: S311
                )
            except ValueError:
                raise GraphConfigurationError() from None

            for connection in connections:
                node.add_connection(connection)
                connection.add_connection(node)

    @classmethod
    def random(  # noqa: PLR0913
        cls,
        *,
        nodes_amount: int = 100,
        connection_percent: int = 80,
        allow_loop_connections: bool = False,
        connection_limit: int = 1,
        min_rand_connections: int = 2,
    ) -> "Graph":
        if connection_percent < cls.connection_percent_cond.min or connection_percent > cls.connection_percent_cond.max:
            raise ConnectionPercentViolationError() from None

        if nodes_amount < cls.nodes_amount_cond.min or nodes_amount > cls.nodes_amount_cond.max:
            raise NodesAmountViolationError() from None

        _min_connections: int = 2
        if min_rand_connections < _min_connections or min_rand_connections > (nodes_amount / 2) + 1:
            raise MinRandConnectionsViolationError() from None

        graph: Graph = cls(
            [Node(idx) for idx in range(nodes_amount)],
            allow_loop_connections=allow_loop_connections,
            connection_percent=connection_percent,
            connection_limit=connection_limit,
        )
        try:
            graph.populate_nodes(min_rand_connections)
        except GraphConfigurationError:
            raise

        return graph
