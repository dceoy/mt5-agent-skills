# MT5 Trade Return Codes

## Success Codes

| Code | Constant | Description |
|------|----------|-------------|
| 10009 | TRADE_RETCODE_DONE | Request completed successfully |
| 10008 | TRADE_RETCODE_PLACED | Order placed |
| 10010 | TRADE_RETCODE_DONE_PARTIAL | Only part of the request was completed |

## Error Codes

| Code | Constant | Description |
|------|----------|-------------|
| 10004 | TRADE_RETCODE_REQUOTE | Requote |
| 10006 | TRADE_RETCODE_REJECT | Request rejected |
| 10007 | TRADE_RETCODE_CANCEL | Request canceled by trader |
| 10011 | TRADE_RETCODE_ERROR | Request processing error |
| 10012 | TRADE_RETCODE_TIMEOUT | Request canceled by timeout |
| 10013 | TRADE_RETCODE_INVALID | Invalid request |
| 10014 | TRADE_RETCODE_INVALID_VOLUME | Invalid volume in the request |
| 10015 | TRADE_RETCODE_INVALID_PRICE | Invalid price in the request |
| 10016 | TRADE_RETCODE_INVALID_STOPS | Invalid stops in the request |
| 10017 | TRADE_RETCODE_TRADE_DISABLED | Trade is disabled |
| 10018 | TRADE_RETCODE_MARKET_CLOSED | Market is closed |
| 10019 | TRADE_RETCODE_NO_MONEY | Not enough money |
| 10020 | TRADE_RETCODE_PRICE_CHANGED | Prices changed |
| 10021 | TRADE_RETCODE_PRICE_OFF | No quotes to process |
| 10022 | TRADE_RETCODE_INVALID_EXPIRATION | Invalid order expiration |
| 10023 | TRADE_RETCODE_ORDER_CHANGED | Order state changed |
| 10024 | TRADE_RETCODE_TOO_MANY_REQUESTS | Too frequent requests |
| 10025 | TRADE_RETCODE_NO_CHANGES | No changes in request |
| 10026 | TRADE_RETCODE_SERVER_DISABLES_AT | Autotrading disabled by server |
| 10027 | TRADE_RETCODE_CLIENT_DISABLES_AT | Autotrading disabled by client |
| 10028 | TRADE_RETCODE_LOCKED | Request locked for processing |
| 10029 | TRADE_RETCODE_FROZEN | Order or position frozen |
| 10030 | TRADE_RETCODE_INVALID_FILL | Invalid order filling type |
| 10031 | TRADE_RETCODE_CONNECTION | No connection with trade server |
| 10032 | TRADE_RETCODE_ONLY_REAL | Operation allowed only for live accounts |
| 10033 | TRADE_RETCODE_LIMIT_ORDERS | Pending orders limit reached |
| 10034 | TRADE_RETCODE_LIMIT_VOLUME | Volume limit for orders/positions reached |
| 10035 | TRADE_RETCODE_INVALID_ORDER | Incorrect or prohibited order type |
| 10036 | TRADE_RETCODE_POSITION_CLOSED | Position already closed |

## Common Error Handling

```python
RETCODE_SUCCESS = {10008, 10009, 10010}

result = client.place_market_order(...)

if result.retcode in RETCODE_SUCCESS:
    print("Order successful")
elif result.retcode == 10019:
    print("Insufficient funds")
elif result.retcode == 10018:
    print("Market closed")
elif result.retcode == 10016:
    print("Invalid stop loss or take profit")
else:
    print(f"Error {result.retcode}: {result.comment}")
```
