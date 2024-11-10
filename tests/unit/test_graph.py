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


class TestNodeCase:
    def test_node_setter_should_raise_value_error_when_the_same_node_is_provided(self):
        node: Node = Node(None)
        with raises(ValueError):
            node.next = node
