---
name: mt5-analysis
description: |
  Perform trading analysis calculations on MetaTrader 5 using pdmt5 library. Use when you need to:
  (1) Calculate margin requirements for a trade
  (2) Calculate potential profit/loss for a trade
  (3) Determine maximum tradeable volume for given margin
  (4) Analyze spread and trading costs
  (5) Assess position sizing and risk management
  Requires active MT5 connection (use mt5-connection skill first).
---

# MT5 Analysis

Calculate margin, profit, volume, and spread for trading decisions.

## Margin Calculation

Calculate required margin for a trade:

```python
margin = client.calculate_minimum_order_margin(
    symbol="EURUSD",
    volume=0.1,           # Lot size
    order_side="BUY"      # or "SELL"
)
print(f"Required margin: {margin}")
```

## Profit Calculation

Calculate potential profit/loss:

```python
import MetaTrader5 as mt5

profit = client.order_calc_profit(
    action=mt5.ORDER_TYPE_BUY,  # or ORDER_TYPE_SELL
    symbol="EURUSD",
    volume=0.1,
    price_open=1.1000,
    price_close=1.1050
)
print(f"Potential profit: {profit}")
```

## Maximum Volume

Find maximum tradeable volume for given margin:

```python
max_volume = client.calculate_volume_by_margin(
    symbol="EURUSD",
    margin=1000,          # Available margin
    order_side="BUY"
)
print(f"Maximum volume: {max_volume} lots")
```

## Spread Analysis

Calculate current spread:

```python
spread_ratio = client.calculate_spread_ratio(symbol="EURUSD")

# Get raw spread data
tick = client.symbol_info_tick(symbol="EURUSD")
symbol_info = client.symbol_info(symbol="EURUSD")

spread_points = tick.ask - tick.bid
spread_pips = spread_points / symbol_info.point

print(f"Spread: {spread_pips} pips ({spread_ratio:.4%})")
```

## Account Metrics

Get account margin status:

```python
account = client.account_info_as_dict()

print(f"Balance: {account['balance']}")
print(f"Equity: {account['equity']}")
print(f"Margin Used: {account['margin']}")
print(f"Free Margin: {account['margin_free']}")
print(f"Margin Level: {account['margin_level']}%")
print(f"Leverage: 1:{account['leverage']}")
```

## Position Metrics

Get positions with calculated metrics:

```python
positions_df = client.fetch_positions_with_metrics_as_df()

# Columns include:
# - profit: Current P/L
# - swap: Swap charges
# - price_current: Current price
# - price_open: Entry price
```

## Risk Calculations

### Position Size by Risk

```python
def calculate_lot_size(
    client,
    symbol: str,
    risk_amount: float,
    stop_loss_pips: float
) -> float:
    """Calculate lot size based on risk amount and stop loss."""
    symbol_info = client.symbol_info(symbol)

    # Get pip value for 1 lot
    tick = client.symbol_info_tick(symbol)
    pip_value = symbol_info.trade_tick_value

    # Calculate lot size
    lot_size = risk_amount / (stop_loss_pips * pip_value)

    # Round to symbol's volume step
    lot_size = round(lot_size / symbol_info.volume_step) * symbol_info.volume_step

    # Clamp to min/max
    lot_size = max(symbol_info.volume_min, min(lot_size, symbol_info.volume_max))

    return lot_size
```

### Risk Percentage

```python
def calculate_risk_percent(
    client,
    symbol: str,
    volume: float,
    stop_loss_pips: float
) -> float:
    """Calculate risk as percentage of account balance."""
    account = client.account_info_as_dict()
    symbol_info = client.symbol_info(symbol)

    pip_value = symbol_info.trade_tick_value * volume
    risk_amount = stop_loss_pips * pip_value
    risk_percent = (risk_amount / account['balance']) * 100

    return risk_percent
```

## Scripts

Use `scripts/analyze_trade.py` for quick trade analysis from command line.
