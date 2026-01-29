#!/usr/bin/env python3
"""MT5 connection context manager for automatic session management."""

from contextlib import contextmanager
from typing import Generator

from pdmt5 import Mt5Config, Mt5TradingClient


@contextmanager
def mt5_session(
    login: int,
    password: str,
    server: str,
    timeout: int = 60000,
    path: str | None = None,
) -> Generator[Mt5TradingClient, None, None]:
    """Context manager for MT5 connections.

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        timeout: Connection timeout in milliseconds
        path: Optional path to MT5 terminal executable

    Yields:
        Connected Mt5TradingClient instance

    Example:
        with mt5_session(12345678, "password", "Broker-Server") as client:
            account = client.account_info_as_dict()
            print(f"Balance: {account['balance']}")
    """
    config = Mt5Config(
        login=login,
        password=password,
        server=server,
        timeout=timeout,
        path=path,
    )
    client = Mt5TradingClient(config=config)

    try:
        client.initialize_and_login_mt5()
        yield client
    finally:
        try:
            client.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test MT5 connection")
    parser.add_argument("--login", type=int, required=True, help="MT5 account number")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--server", required=True, help="Broker server name")
    args = parser.parse_args()

    with mt5_session(args.login, args.password, args.server) as client:
        account = client.account_info_as_dict()
        print(f"Connected to: {account['name']}")
        print(f"Balance: {account['balance']} {account['currency']}")
        print(f"Equity: {account['equity']} {account['currency']}")
