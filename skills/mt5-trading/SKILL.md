---
name: mt5-trading
description: |
  Execute trades and manage positions on MetaTrader 5 using pdmt5 library. Use when you need to:
  (1) Place market orders (buy/sell at current price)
  (2) View and manage open positions
  (3) Close positions (single or all)
  (4) Update stop loss and take profit levels
  (5) View pending orders and order history
  (6) Access trade history and deals
  Requires active MT5 connection (use mt5-connection skill first).
  CAUTION: Trading involves financial risk. Use dry_run=True for testing.
---

# MT5 Trading

Execute trades and manage positions using pdmt5.

## Place Market Order

```python
result = client.place_market_order(
    symbol="EURUSD",
    volume=0.01,           # Lot size
    order_side="BUY",      # or "SELL"
    sl=None,               # Stop loss price (optional)
    tp=None,               # Take profit price (optional)
    deviation=20,          # Max slippage in points
    comment="",            # Order comment
    magic=0,               # Magic number for identification
    dry_run=False          # Set True to validate without executing
)

# Check result
if result.retcode == 10009:  # TRADE_RETCODE_DONE
    print(f"Order placed: deal={result.deal}, order={result.order}")
else:
    print(f"Failed: {result.comment}")
```

## View Positions

```python
# All positions as DataFrame
positions_df = client.fetch_positions_with_metrics_as_df()
# Columns: ticket, time, symbol, type, volume, price_open, sl, tp,
#          price_current, profit, swap, magic, comment

# Filter by symbol
positions_df = client.fetch_positions_with_metrics_as_df(symbols=["EURUSD"])

# As raw tuples
positions = client.positions_get()
positions = client.positions_get(symbol="EURUSD")
```

## Close Positions

```python
# Close all positions for specific symbols
results = client.close_open_positions(
    symbols=["EURUSD", "GBPUSD"],
    comment="Closing positions",
    deviation=20
)

# Close all positions (no symbols filter)
results = client.close_open_positions()

# Close positions with specific magic number
results = client.close_open_positions(magic=12345)
```

## Update Stop Loss / Take Profit

```python
# Update SL/TP for all positions of a symbol
results = client.update_sltp_for_open_positions(
    symbol="EURUSD",
    sl=1.0800,  # New stop loss
    tp=1.1200   # New take profit
)
```

## Pending Orders

```python
# All pending orders as DataFrame
orders_df = client.orders_get_as_df()

# Filter by symbol
orders_df = client.orders_get_as_df(symbol="EURUSD")
```

## Order History

```python
from datetime import datetime, timedelta

# History for date range
orders_df = client.history_orders_get_as_df(
    date_from=datetime.now() - timedelta(days=30),
    date_to=datetime.now()
)

# Filter by symbol
orders_df = client.history_orders_get_as_df(symbol="EURUSD")
```

## Deal History

```python
# All deals in date range
deals_df = client.history_deals_get_as_df(
    date_from=datetime.now() - timedelta(days=30),
    date_to=datetime.now()
)
```

## Order Return Codes

| Code | Constant | Meaning |
|------|----------|---------|
| 10009 | TRADE_RETCODE_DONE | Request completed |
| 10008 | TRADE_RETCODE_PLACED | Order placed |
| 10010 | TRADE_RETCODE_DONE_PARTIAL | Partial fill |
| 10006 | TRADE_RETCODE_REJECT | Request rejected |
| 10004 | TRADE_RETCODE_REQUOTE | Requote |

See `references/return_codes.md` for complete list.

## Safety

- Always use `dry_run=True` first to validate orders
- Verify account has sufficient margin before trading
- Use `scripts/place_order.py` for command-line testing
