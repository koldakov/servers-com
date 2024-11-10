from argparse import ArgumentParser, Namespace

from servers_com.ui import Application


def _parse_args() -> Namespace:
    parser = ArgumentParser(
        description="Personal information",
    )
    parser.add_argument(
        "--nodes-amount",
        dest="nodes_amount",
        type=int,
        help="Nodes amount. Default is 100.",
        default=100,
    )
    parser.add_argument(
        "--connection-percent",
        dest="connection_percent",
        type=int,
        help="Connection percent. Must be between 1 and 100. Default is 80.",
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

    app: Application = Application(
        args.nodes_amount,
        args.connection_percent,
        edge_size=args.edge_size,
    )
    app.visualize()
