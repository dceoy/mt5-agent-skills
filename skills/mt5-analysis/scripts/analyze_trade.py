#!/usr/bin/env python3
"""Analyze trade parameters including margin, profit, and risk."""

import argparse
import json

import MetaTrader5 as mt5
from pdmt5 import Mt5Config, Mt5TradingClient


def analyze_trade(
    login: int,
    password: str,
    server: str,
    symbol: str,
    volume: float,
    side: str,
    entry_price: float | None = None,
    exit_price: float | None = None,
    stop_loss: float | None = None,
    take_profit: float | None = None,
) -> dict:
    """Analyze a potential trade.

    Args:
        login: MT5 account number
        password: Account password
        server: Broker server name
        symbol: Trading symbol
        volume: Lot size
        side: Order side (BUY or SELL)
        entry_price: Entry price (uses current price if None)
        exit_price: Exit price for profit calculation
        stop_loss: Stop loss price
        take_profit: Take profit price

    Returns:
        Analysis results dictionary
    """
    config = Mt5Config(login=login, password=password, server=server)
    client = Mt5TradingClient(config=config)

    try:
        client.initialize_and_login_mt5()

        # Get account info
        account = client.account_info_as_dict()

        # Get symbol info
        symbol_info = client.symbol_info(symbol)
        tick = client.symbol_info_tick(symbol)

        if symbol_info is None or tick is None:
            return {"error": f"Symbol {symbol} not found"}

        side_upper = side.upper()
        action = mt5.ORDER_TYPE_BUY if side_upper == "BUY" else mt5.ORDER_TYPE_SELL

        # Use current price if not specified
        if entry_price is None:
            entry_price = tick.ask if side_upper == "BUY" else tick.bid

        # Calculate margin
        margin = client.calculate_minimum_order_margin(
            symbol=symbol,
            volume=volume,
            order_side=side_upper,
        )

        # Calculate spread
        spread_points = tick.ask - tick.bid
        spread_pips = spread_points / symbol_info.point

        # Calculate profit if exit price given
        profit = None
        if exit_price:
            profit = client.order_calc_profit(
                action=action,
                symbol=symbol,
                volume=volume,
                price_open=entry_price,
                price_close=exit_price,
            )

        # Calculate SL/TP profit
        sl_profit = None
        tp_profit = None

        if stop_loss:
            sl_profit = client.order_calc_profit(
                action=action,
                symbol=symbol,
                volume=volume,
                price_open=entry_price,
                price_close=stop_loss,
            )

        if take_profit:
            tp_profit = client.order_calc_profit(
                action=action,
                symbol=symbol,
                volume=volume,
                price_open=entry_price,
                price_close=take_profit,
            )

        # Calculate risk/reward ratio
        risk_reward = None
        if sl_profit and tp_profit and sl_profit < 0:
            risk_reward = abs(tp_profit / sl_profit)

        return {
            "symbol": symbol,
            "side": side_upper,
            "volume": volume,
            "entry_price": entry_price,
            "account": {
                "balance": account["balance"],
                "equity": account["equity"],
                "margin_free": account["margin_free"],
                "currency": account["currency"],
            },
            "margin": {
                "required": margin,
                "available": account["margin_free"],
                "sufficient": margin <= account["margin_free"] if margin else None,
            },
            "spread": {
                "points": spread_points,
                "pips": spread_pips,
            },
            "profit_calc": {
                "exit_price": exit_price,
                "profit": profit,
            }
            if exit_price
            else None,
            "stop_loss": {
                "price": stop_loss,
                "profit": sl_profit,
                "risk_percent": (abs(sl_profit) / account["balance"] * 100)
                if sl_profit
                else None,
            }
            if stop_loss
            else None,
            "take_profit": {
                "price": take_profit,
                "profit": tp_profit,
            }
            if take_profit
            else None,
            "risk_reward_ratio": risk_reward,
        }

    finally:
        try:
            client.shutdown()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Analyze trade parameters")
    parser.add_argument("--login", type=int, required=True, help="MT5 account number")
    parser.add_argument("--password", required=True, help="Account password")
    parser.add_argument("--server", required=True, help="Broker server name")
    parser.add_argument("--symbol", required=True, help="Trading symbol")
    parser.add_argument("--volume", type=float, required=True, help="Lot size")
    parser.add_argument(
        "--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side"
    )
    parser.add_argument("--entry", type=float, help="Entry price (uses current if omitted)")
    parser.add_argument("--exit", type=float, help="Exit price for profit calculation")
    parser.add_argument("--sl", type=float, help="Stop loss price")
    parser.add_argument("--tp", type=float, help="Take profit price")

    args = parser.parse_args()

    result = analyze_trade(
        login=args.login,
        password=args.password,
        server=args.server,
        symbol=args.symbol,
        volume=args.volume,
        side=args.side,
        entry_price=args.entry,
        exit_price=args.exit,
        stop_loss=args.sl,
        take_profit=args.tp,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
