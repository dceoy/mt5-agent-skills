---
name: mt5-connection
description: |
  Connect to MetaTrader 5 trading platform using pdmt5 library. Use when you need to:
  (1) Initialize MT5 terminal connection with login credentials
  (2) Get account information (balance, equity, margin, leverage)
  (3) Get terminal information (version, connection status, trade permissions)
  (4) Manage MT5 session lifecycle (connect/disconnect)
  Required before using any other MT5 skills. Works on Windows only.
---

# MT5 Connection

Manage MetaTrader 5 terminal connections using pdmt5.

## Prerequisites

- Windows OS (MT5 requirement)
- MetaTrader 5 terminal installed
- pdmt5 package: `pip install pdmt5`

## Connection

Initialize and connect to MT5:

```python
from pdmt5 import Mt5Config, Mt5TradingClient

config = Mt5Config(
    login=12345678,           # MT5 account number
    password="your_password", # Account password
    server="Broker-Server",   # Broker server name
    timeout=60000,            # Connection timeout (ms)
    path=None                 # Optional: path to terminal64.exe
)

client = Mt5TradingClient(config=config)
client.initialize_and_login_mt5()
```

## Account Information

Get account details:

```python
# As dictionary
account = client.account_info_as_dict()
# Keys: login, balance, equity, margin, margin_free, margin_level,
#       leverage, currency, profit, credit, name, server, trade_mode

# As DataFrame
account_df = client.account_info_as_df()
```

## Terminal Information

Get terminal status:

```python
terminal = client.terminal_info()
# Attributes: community_account, community_connection, connected,
#             dlls_allowed, trade_allowed, tradeapi_disabled,
#             email_enabled, ftp_enabled, notifications_enabled,
#             mqid, build, maxbars, codepage, ping_last, name, path
```

## Disconnect

Always disconnect when done:

```python
client.shutdown()
```

## Context Manager Pattern

For automatic cleanup, use the script in `scripts/mt5_context.py`.

## Error Handling

Connection failures raise exceptions. Always wrap in try/except:

```python
try:
    client.initialize_and_login_mt5()
except Exception as e:
    print(f"Connection failed: {e}")
```

## Common Issues

- **"Terminal not found"**: Set `path` to terminal64.exe location
- **"Invalid account"**: Verify login/password/server
- **"Timeout"**: Increase timeout value or check network
