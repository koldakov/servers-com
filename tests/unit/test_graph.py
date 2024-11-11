from pytest import raises

from servers_com.graph import ConnectionPercentViolationError, Graph, Node, NodesAmountViolationError


class TestGraphRandomCase:
    def test_random_should_raise_nodes_amount_violation_error_when_nodes_amount_is_negative_one(self):
        with raises(NodesAmountViolationError):
            Graph.random(nodes_amount=-1)

    def test_random_should_raise_nodes_amount_violation_error_when_nodes_amount_is_999999(self):
        with raises(NodesAmountViolationError):
            Graph.random(nodes_amount=999999)

    def test_random_should_raise_connection_percent_violation_error_when_connection_percent_is_negative_one(self):
        with raises(ConnectionPercentViolationError):
            Graph.random(connection_percent=-1)

    def test_random_should_raise_connection_percent_violation_error_when_connection_percent_is_101(self):
        with raises(ConnectionPercentViolationError):
            Graph.random(connection_percent=101)

    def test_random_should_return_4_nodes_graph_when_nodes_amount_is_4(self):
        nodes_amount: int = 4
        graph: Graph = Graph.random(nodes_amount=nodes_amount)

        assert len(graph.nodes) == nodes_amount

    def test_set_limits_sets_two_connection_limits_when_eight_nodes_provided(self):
        graph: Graph = Graph([Node(n) for n in range(8)])
        assert not graph.limited_nodes

        graph.set_limits()

        assert len([n for n in graph.nodes if n.connections_limit is not None]) == 2  # noqa: PLR2004
