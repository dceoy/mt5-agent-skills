#!/usr/bin/env python3
"""Close open positions on MT5."""

import argparse
import json
import sys

from pdmt5 import Mt5Config, Mt5TradingClient


def close_positions(
    login: int,
    password: str,
    server: str,
    symbols: list[str] | None = None,
    magic: int | None = None,
    comment: str = "",
) -> dict:
    """Close open positions on MT5.

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        symbols: List of symbols to close (None = all)
        magic: Only close positions with this magic number
        comment: Comment for close orders

    Returns:
        Close results dictionary
    """
    config = Mt5Config(login=login, password=password, server=server)
    client = Mt5TradingClient(config=config)

    try:
        client.initialize_and_login_mt5()

        # Get current positions first
        positions_df = client.fetch_positions_with_metrics_as_df(symbols=symbols)

        if positions_df is None or positions_df.empty:
            return {
                "closed_count": 0,
                "results": [],
                "message": "No open positions found",
            }

        # Close positions
        close_kwargs = {"comment": comment, "deviation": 20}
        if symbols:
            close_kwargs["symbols"] = symbols
        if magic is not None:
            close_kwargs["magic"] = magic

        results = client.close_open_positions(**close_kwargs)

        if not results:
            return {
                "closed_count": 0,
                "results": [],
                "message": "No positions closed",
            }

        results_data = []
        for r in results:
            results_data.append({
                "retcode": r.retcode,
                "deal": r.deal,
                "order": r.order,
                "volume": r.volume,
                "price": r.price,
                "comment": r.comment,
                "success": r.retcode == 10009,
            })

        return {
            "closed_count": len(results_data),
            "results": results_data,
            "message": f"Closed {len(results_data)} position(s)",
        }

    finally:
        try:
            client.shutdown()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Close open positions on MT5")
    parser.add_argument("--login", type=int, required=True, help="MT5 account number")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--server", required=True, help="Broker server name")
    parser.add_argument(
        "--symbols", nargs="+", help="Symbols to close (default: all)"
    )
    parser.add_argument("--magic", type=int, help="Only close positions with this magic")
    parser.add_argument("--comment", default="", help="Comment for close orders")

    args = parser.parse_args()

    result = close_positions(
        login=args.login,
        password=args.password,
        server=args.server,
        symbols=args.symbols,
        magic=args.magic,
        comment=args.comment,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
