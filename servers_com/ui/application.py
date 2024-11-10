import matplotlib.pyplot
from networkx import DiGraph, draw, spring_layout

from servers_com.graph import Graph
from servers_com.utils import metadata


class Application:
    def __init__(
        self,
        nodes_amount: int,
        connection_percent: int,
        /,
        *,
        edge_size: int | None = None,
    ) -> None:
        self.edge_size: int | None = edge_size
        self.connection_percent: int = connection_percent

        self.graph: Graph = Graph.random(
            nodes_amount=nodes_amount,
            connection_percent=connection_percent,
        )
        self.di_graph: DiGraph = DiGraph()

    @property
    def di_graph(self) -> DiGraph:
        return self._di_graph

    @di_graph.setter
    def di_graph(self, graph: DiGraph, /) -> None:
        for node in self.graph.nodes:
            if node.next is not None:
                graph.add_edge(hash(node), hash(node.next))
            else:
                graph.add_node(hash(node))

        self._di_graph = graph

    def draw(self, pos: dict, /) -> None:
        draw(
            self.di_graph,
            pos,
            with_labels=True,
            arrows=True,
        )

    @property
    def layout(self) -> dict:
        return spring_layout(
            self.di_graph,
            k=self.edge_size,
        )

    @property
    def title(self) -> str:
        return (
            f"Graph with single 'next' connection per Node. Graph has {len(self.graph.nodes)} "
            f"nodes with connection percent={self.connection_percent}. Ver. {metadata["version"]}."
        )

    def visualize(self):
        matplotlib.pyplot.figure(
            f"graph_{len(self.graph.nodes)}_{self.connection_percent}",
            figsize=(
                12,
                12,
            ),
        )
        matplotlib.pyplot.title(self.title)

        self.draw(self.layout)

        matplotlib.pyplot.show()
