# MT5 Timeframes Reference

## Timeframe Constants

```python
import MetaTrader5 as mt5

# Minutes
mt5.TIMEFRAME_M1   # 1 minute
mt5.TIMEFRAME_M2   # 2 minutes
mt5.TIMEFRAME_M3   # 3 minutes
mt5.TIMEFRAME_M4   # 4 minutes
mt5.TIMEFRAME_M5   # 5 minutes
mt5.TIMEFRAME_M6   # 6 minutes
mt5.TIMEFRAME_M10  # 10 minutes
mt5.TIMEFRAME_M12  # 12 minutes
mt5.TIMEFRAME_M15  # 15 minutes
mt5.TIMEFRAME_M20  # 20 minutes
mt5.TIMEFRAME_M30  # 30 minutes

# Hours
mt5.TIMEFRAME_H1   # 1 hour
mt5.TIMEFRAME_H2   # 2 hours
mt5.TIMEFRAME_H3   # 3 hours
mt5.TIMEFRAME_H4   # 4 hours
mt5.TIMEFRAME_H6   # 6 hours
mt5.TIMEFRAME_H8   # 8 hours
mt5.TIMEFRAME_H12  # 12 hours

# Daily and above
mt5.TIMEFRAME_D1   # 1 day
mt5.TIMEFRAME_W1   # 1 week
mt5.TIMEFRAME_MN1  # 1 month
```

## pdmt5 Granularity Strings

When using `fetch_latest_rates_as_df`, use string granularities:

| String | Equivalent |
|--------|------------|
| "M1" | TIMEFRAME_M1 |
| "M2" | TIMEFRAME_M2 |
| "M3" | TIMEFRAME_M3 |
| "M4" | TIMEFRAME_M4 |
| "M5" | TIMEFRAME_M5 |
| "M6" | TIMEFRAME_M6 |
| "M10" | TIMEFRAME_M10 |
| "M12" | TIMEFRAME_M12 |
| "M15" | TIMEFRAME_M15 |
| "M20" | TIMEFRAME_M20 |
| "M30" | TIMEFRAME_M30 |
| "H1" | TIMEFRAME_H1 |
| "H2" | TIMEFRAME_H2 |
| "H3" | TIMEFRAME_H3 |
| "H4" | TIMEFRAME_H4 |
| "H6" | TIMEFRAME_H6 |
| "H8" | TIMEFRAME_H8 |
| "H12" | TIMEFRAME_H12 |
| "D1" | TIMEFRAME_D1 |
| "W1" | TIMEFRAME_W1 |
| "MN1" | TIMEFRAME_MN1 |

## Data Availability

- Minute data: Usually 1-2 years
- Hourly data: Usually 5+ years
- Daily data: Full history available
- Data availability varies by broker
