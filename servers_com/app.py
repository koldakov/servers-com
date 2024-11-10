from argparse import ArgumentParser, ArgumentTypeError, Namespace

from servers_com.graph import ConnectionPercentViolationError, Graph, NodesAmountViolationError
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

    return parser.parse_args()


def run():
    args: Namespace = _parse_args()

    try:
        app: Application = Application(
            args.nodes_amount,
            args.connection_percent,
            edge_size=args.edge_size,
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

    app.visualize()
