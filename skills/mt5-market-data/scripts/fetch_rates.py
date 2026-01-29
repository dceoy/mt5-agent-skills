#!/usr/bin/env python3
"""Fetch OHLCV rates from MT5 and output as CSV or JSON."""

import argparse
import json
import sys
from datetime import datetime

from pdmt5 import Mt5Config, Mt5TradingClient


def fetch_rates(
    login: int,
    password: str,
    server: str,
    symbol: str,
    timeframe: str = "H1",
    count: int = 100,
    output_format: str = "csv",
) -> str:
    """Fetch OHLCV rates from MT5.

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        symbol: Trading symbol (e.g., EURUSD)
        timeframe: Timeframe (M1, M5, M15, M30, H1, H4, D1, W1, MN1)
        count: Number of bars to fetch
        output_format: Output format (csv or json)

    Returns:
        Formatted rates data
    """
    config = Mt5Config(login=login, password=password, server=server)
    client = Mt5TradingClient(config=config)

    try:
        client.initialize_and_login_mt5()

        rates_df = client.fetch_latest_rates_as_df(
            symbol=symbol,
            granularity=timeframe,
            count=count,
        )

        if rates_df is None or rates_df.empty:
            return f"No data found for {symbol}"

        rates_df = rates_df.reset_index()

        if output_format == "json":
            return rates_df.to_json(orient="records", date_format="iso", indent=2)
        else:
            return rates_df.to_csv(index=False)

    finally:
        try:
            client.shutdown()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Fetch OHLCV rates from MT5")
    parser.add_argument("--login", type=int, required=True, help="MT5 account number")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--server", required=True, help="Broker server name")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., EURUSD)")
    parser.add_argument(
        "--timeframe",
        default="H1",
        choices=["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN1"],
        help="Timeframe (default: H1)",
    )
    parser.add_argument(
        "--count", type=int, default=100, help="Number of bars (default: 100)"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    args = parser.parse_args()

    result = fetch_rates(
        login=args.login,
        password=args.password,
        server=args.server,
        symbol=args.symbol,
        timeframe=args.timeframe,
        count=args.count,
        output_format=args.format,
    )

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
