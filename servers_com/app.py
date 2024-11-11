import sys
from argparse import ArgumentParser, ArgumentTypeError, BooleanOptionalAction, Namespace

from servers_com.graph import (
    ConnectionPercentViolationError,
    Graph,
    GraphConfigurationError,
    MinRandConnectionsViolationError,
    NodesAmountViolationError,
)
from servers_com.ui import Application, EdgeSizeViolationError


def _parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Personal information",
    )
    parser.add_argument(
        "--nodes-amount",
        dest="nodes_amount",
        type=int,
        help=f"Nodes amount. Default is 100. Must be between {Graph.nodes_amount_cond.min} "
        f"and {Graph.nodes_amount_cond.max}.",
        default=100,
    )
    parser.add_argument(
        "--connection-percent",
        dest="connection_percent",
        type=int,
        help=f"Connection percent. Must be between {Graph.connection_percent_cond.min} "
        f"and {Graph.connection_percent_cond.max}. Default is 80.",
        default=80,
    )
    parser.add_argument(
        "--edge-size",
        dest="edge_size",
        type=int,
        help="Optimal distance between nodes. Must be more than 0.",
    )
    parser.add_argument(
        "--allow-loops",
        dest="allow_loops",
        action=BooleanOptionalAction,
        default=False,
        help="Allow nodes to be connected to itself.",
    )
    parser.add_argument(
        "--cli-only",
        dest="cli_only",
        action=BooleanOptionalAction,
        default=False,
        help="Print nodes in format: [(node_id, connection_limit, [connection_1, connection_2]),].",
    )
    parser.add_argument(
        "--min-rand-connections",
        dest="min_rand_connections",
        type=int,
        default=2,
        help="Connections for --connection-percent selected randomly between 2 and --min-rand-connections. "
        "Keep in mind this option does not guarantee than connection has exactly or less than "
        "--min-rand-connections connections.",
    )

    return parser.parse_args()


def run():
    args: Namespace = _parse_args()

    try:
        app: Application = Application(
            args.nodes_amount,
            args.connection_percent,
            args.allow_loops,
            edge_size=args.edge_size,
            min_rand_connections=args.min_rand_connections,
        )
    except ConnectionPercentViolationError:
        raise ArgumentTypeError(
            f"--connection-percent must be between {Graph.connection_percent_cond.min} "
            f"and {Graph.connection_percent_cond.max}"
        ) from None
    except NodesAmountViolationError:
        raise ArgumentTypeError(
            f"--nodes-amount must be between {Graph.nodes_amount_cond.min} " f"and {Graph.nodes_amount_cond.max}"
        ) from None
    except EdgeSizeViolationError:
        raise ArgumentTypeError("--edge-size must be more than 0") from None
    except MinRandConnectionsViolationError:
        raise ArgumentTypeError(
            "--min-rand-connections must be more than 2 and less than (nodes-amount / 2 + 1)"
        ) from None
    except GraphConfigurationError:
        raise ArgumentTypeError(
            "Graph configurations error. " "Perhaps, there are not enough edges to meet the requirements."
        ) from None

    if args.cli_only is False:
        app.visualize()
    else:
        sys.stdout.write(str(app.graph.human_readable_nodes()))
