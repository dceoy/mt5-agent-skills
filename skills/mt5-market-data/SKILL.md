---
name: mt5-market-data
description: |
  Retrieve market data from MetaTrader 5 using pdmt5 library. Use when you need to:
  (1) Get available trading symbols and their specifications
  (2) Fetch current bid/ask prices and tick data
  (3) Retrieve OHLCV (candlestick) historical price data
  (4) Get tick-by-tick data for high-frequency analysis
  Requires active MT5 connection (use mt5-connection skill first).
---

# MT5 Market Data

Retrieve symbols, prices, and historical data from MetaTrader 5.

## Symbols

### List Available Symbols

```python
# Get all symbols
symbols = client.symbols_get()
symbol_names = [s.name for s in symbols]

# Filter by group pattern
forex_symbols = client.symbols_get(group="*USD*")
```

### Symbol Information

```python
# As dictionary (recommended)
info = client.symbol_info_as_dict(symbol="EURUSD")
# Keys: name, bid, ask, spread, digits, point, trade_mode,
#       volume_min, volume_max, volume_step, trade_contract_size,
#       margin_initial, currency_base, currency_profit

# As named tuple
info = client.symbol_info(symbol="EURUSD")
```

## Current Prices

### Get Current Tick

```python
# As dictionary
tick = client.symbol_info_tick_as_dict(symbol="EURUSD")
# Keys: time, bid, ask, last, volume, flags

# As named tuple
tick = client.symbol_info_tick(symbol="EURUSD")
```

## Historical Rates (OHLCV)

### Fetch Latest Bars

```python
# Get last N bars as DataFrame
rates_df = client.fetch_latest_rates_as_df(
    symbol="EURUSD",
    granularity="H1",  # Timeframe
    count=100          # Number of bars
)
# Columns: time (index), open, high, low, close, tick_volume, spread, real_volume
```

### Fetch by Date Range

```python
import MetaTrader5 as mt5
from datetime import datetime

rates_df = client.copy_rates_range_as_df(
    symbol="EURUSD",
    timeframe=mt5.TIMEFRAME_H1,
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 1, 31)
)
```

### Timeframes

| Granularity | MT5 Constant | Description |
|-------------|--------------|-------------|
| M1 | TIMEFRAME_M1 | 1 minute |
| M5 | TIMEFRAME_M5 | 5 minutes |
| M15 | TIMEFRAME_M15 | 15 minutes |
| M30 | TIMEFRAME_M30 | 30 minutes |
| H1 | TIMEFRAME_H1 | 1 hour |
| H4 | TIMEFRAME_H4 | 4 hours |
| D1 | TIMEFRAME_D1 | 1 day |
| W1 | TIMEFRAME_W1 | 1 week |
| MN1 | TIMEFRAME_MN1 | 1 month |

## Tick Data

### Get Recent Ticks

```python
# Last N seconds of tick data
ticks_df = client.fetch_latest_ticks_as_df(
    symbol="EURUSD",
    seconds=60  # Last 60 seconds
)
# Columns: time (index), bid, ask, last, volume, flags
```

## Scripts

Use `scripts/fetch_rates.py` for quick data retrieval from command line.

## References

See `references/timeframes.md` for complete timeframe mappings.
