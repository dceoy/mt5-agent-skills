# mt5-agent-skills

Agent Skills for MetaTrader 5 using [pdmt5](https://github.com/dceoy/pdmt5).

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Overview

This repository contains Agent Skills in the [Anthropic Skills format](https://github.com/anthropics/skills) for interacting with MetaTrader 5 (MT5) trading platform. These skills enable AI agents like Claude to execute trading operations, retrieve market data, and perform analysis.

## Requirements

- Windows OS (required by MetaTrader 5)
- MetaTrader 5 terminal installed
- Python 3.11+
- pdmt5 package: `pip install pdmt5`

## Skills

| Skill | Description |
|-------|-------------|
| [mt5-connection](skills/mt5-connection/) | Connect to MT5, get account/terminal info |
| [mt5-market-data](skills/mt5-market-data/) | Retrieve symbols, prices, and OHLCV data |
| [mt5-trading](skills/mt5-trading/) | Place orders, manage positions |
| [mt5-analysis](skills/mt5-analysis/) | Calculate margin, profit, risk |

## Structure

Each skill follows the Anthropic Skills format:

```
skills/
├── mt5-connection/
│   ├── SKILL.md              # Skill instructions
│   └── scripts/
│       └── mt5_context.py    # Connection context manager
├── mt5-market-data/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── fetch_rates.py    # Fetch OHLCV data
│   └── references/
│       └── timeframes.md     # Timeframe reference
├── mt5-trading/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── place_order.py    # Place market orders
│   │   └── close_positions.py
│   └── references/
│       └── return_codes.md   # Trade return codes
└── mt5-analysis/
    ├── SKILL.md
    └── scripts/
        └── analyze_trade.py  # Trade analysis
```

## Usage with Claude

These skills are designed for use with Claude Code or other AI agents that support the Anthropic Skills format.

### Quick Start

1. Clone this repository
2. Skills will be automatically available when the skill directory is configured

### Manual Usage

Skills can also be used as reference documentation. Each `SKILL.md` contains:
- YAML frontmatter with name and description
- Markdown instructions with code examples
- References to bundled scripts

### Using Scripts Directly

```bash
# Fetch OHLCV rates
python skills/mt5-market-data/scripts/fetch_rates.py \
  --login 12345678 \
  --password "your_password" \
  --server "Broker-Server" \
  --symbol EURUSD \
  --timeframe H1 \
  --count 100

# Analyze a trade
python skills/mt5-analysis/scripts/analyze_trade.py \
  --login 12345678 \
  --password "your_password" \
  --server "Broker-Server" \
  --symbol EURUSD \
  --volume 0.1 \
  --side BUY \
  --sl 1.0800 \
  --tp 1.1200

# Place order (dry run by default)
python skills/mt5-trading/scripts/place_order.py \
  --login 12345678 \
  --password "your_password" \
  --server "Broker-Server" \
  --symbol EURUSD \
  --volume 0.01 \
  --side BUY

# Execute order (add --execute flag)
python skills/mt5-trading/scripts/place_order.py \
  --login 12345678 \
  --password "your_password" \
  --server "Broker-Server" \
  --symbol EURUSD \
  --volume 0.01 \
  --side BUY \
  --execute
```

## Skill Descriptions

### mt5-connection

Initialize and manage MT5 terminal connections. Required before using other skills.

- Connect with login credentials
- Get account information (balance, equity, margin)
- Get terminal information (version, status)
- Context manager for automatic cleanup

### mt5-market-data

Retrieve market data from MT5.

- List available symbols with filtering
- Get symbol specifications
- Fetch current bid/ask prices
- Retrieve OHLCV historical data
- Get tick-by-tick data

### mt5-trading

Execute trades and manage positions.

- Place market orders (buy/sell)
- View open positions with metrics
- Close positions (single or batch)
- Update stop loss and take profit
- View order and deal history

### mt5-analysis

Perform trading calculations.

- Calculate margin requirements
- Calculate potential profit/loss
- Determine maximum volume for margin
- Analyze spread and trading costs
- Risk/reward ratio calculation

## Safety

Trading involves financial risk. The trading skill includes:

- `dry_run=True` mode for order validation without execution
- Scripts default to dry run mode
- Clear documentation of return codes and errors

## Related Projects

- [pdmt5](https://github.com/dceoy/pdmt5) - Pandas-based MetaTrader 5 data handler
- [MetaTrader5](https://pypi.org/project/MetaTrader5/) - Official MT5 Python package
- [Anthropic Skills](https://github.com/anthropics/skills) - Skills format specification

## License

AGPL-3.0 - See [LICENSE](LICENSE) for details.
