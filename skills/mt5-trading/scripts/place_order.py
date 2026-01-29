#!/usr/bin/env python3
"""Place market orders on MT5 with validation."""

import argparse
import json
import sys

from pdmt5 import Mt5Config, Mt5TradingClient


def place_order(
    login: int,
    password: str,
    server: str,
    symbol: str,
    volume: float,
    side: str,
    sl: float | None = None,
    tp: float | None = None,
    comment: str = "",
    magic: int = 0,
    dry_run: bool = True,
) -> dict:
    """Place a market order on MT5.

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        symbol: Trading symbol
        volume: Lot size
        side: Order side (BUY or SELL)
        sl: Stop loss price
        tp: Take profit price
        comment: Order comment
        magic: Magic number
        dry_run: If True, validate only without executing

    Returns:
        Order result dictionary
    """
    config = Mt5Config(login=login, password=password, server=server)
    client = Mt5TradingClient(config=config)

    try:
        client.initialize_and_login_mt5()

        result = client.place_market_order(
            symbol=symbol,
            volume=volume,
            order_side=side.upper(),
            sl=sl,
            tp=tp,
            deviation=20,
            comment=comment,
            magic=magic,
            dry_run=dry_run,
        )

        return {
            "retcode": result.retcode,
            "deal": result.deal,
            "order": result.order,
            "volume": result.volume,
            "price": result.price,
            "bid": result.bid,
            "ask": result.ask,
            "comment": result.comment,
            "dry_run": dry_run,
            "success": result.retcode == 10009,
        }

    finally:
        try:
            client.shutdown()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Place market order on MT5")
    parser.add_argument("--login", type=int, required=True, help="MT5 account number")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--server", required=True, help="Broker server name")
    parser.add_argument("--symbol", required=True, help="Trading symbol")
    parser.add_argument("--volume", type=float, required=True, help="Lot size")
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side"
    )
    parser.add_argument("--sl", type=float, help="Stop loss price")
    parser.add_argument("--tp", type=float, help="Take profit price")
    parser.add_argument("--comment", default="", help="Order comment")
    parser.add_argument("--magic", type=int, default=0, help="Magic number")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute the order (default is dry run)",
    )

    args = parser.parse_args()

    result = place_order(
        login=args.login,
        password=args.password,
        server=args.server,
        symbol=args.symbol,
        volume=args.volume,
        side=args.side,
        sl=args.sl,
        tp=args.tp,
        comment=args.comment,
        magic=args.magic,
        dry_run=not args.execute,
    )

    print(json.dumps(result, indent=2))

    if not result["success"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
