# mt5-agent-skills

Agent Skills for MetaTrader 5 using [pdmt5](https://github.com/dceoy/pdmt5).

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

## Overview

`mt5-agent-skills` provides a set of structured skills that enable AI agents to interact with MetaTrader 5 (MT5) for trading operations. Built on top of `pdmt5`, it offers:

- **Validated Inputs**: All skill parameters are validated using Pydantic models
- **Standardized Outputs**: Consistent `SkillResult` format across all skills
- **Tool Definitions**: Auto-generated tool definitions for AI agent frameworks
- **Categorized Skills**: Skills organized by domain (account, market_data, trading, analysis)

## Requirements

- Python 3.11+
- Windows OS (required by MetaTrader 5)
- MetaTrader 5 terminal installed

## Installation

```bash
pip install mt5-agent-skills
```

Or install from source:

```bash
git clone https://github.com/dceoy/mt5-agent-skills.git
cd mt5-agent-skills
pip install -e .
```

## Quick Start

```python
from mt5_agent_skills import get_registry, get_client_manager

# Configure and connect to MT5
manager = get_client_manager()
manager.configure(
    login=12345678,
    password="your_password",
    server="YourBroker-Server"
)
manager.connect()

# Get the skill registry
registry = get_registry()

# Execute skills
account_info = registry.execute("get_account_info")
print(account_info.to_agent_response())

# Get EURUSD rates
rates = registry.execute(
    "get_latest_rates",
    symbol="EURUSD",
    timeframe="H1",
    count=100
)
print(rates.data)

# Disconnect when done
manager.disconnect()
```

### Using Context Manager

```python
from mt5_agent_skills import mt5_connection, get_registry

with mt5_connection(12345678, "password", "Server"):
    registry = get_registry()

    # Get available symbols
    symbols = registry.execute("get_symbols", group="*USD*")
    print(symbols.data)

    # Place a market order (with dry_run for safety)
    order = registry.execute(
        "place_market_order",
        symbol="EURUSD",
        volume=0.01,
        order_side="BUY",
        dry_run=True
    )
    print(order.data)
```

## Available Skills

### Account Skills

| Skill | Description |
|-------|-------------|
| `get_account_info` | Retrieve account balance, equity, margin, and settings |
| `get_terminal_info` | Get MT5 terminal version and connection status |

### Market Data Skills

| Skill | Description |
|-------|-------------|
| `get_symbols` | List available trading symbols with optional filtering |
| `get_symbol_info` | Get detailed symbol specifications and trading conditions |
| `get_tick` | Get current bid/ask prices for a symbol |
| `get_latest_rates` | Fetch recent OHLCV bars for a symbol |
| `get_rates_range` | Get OHLCV data for a specific date range |
| `get_latest_ticks` | Get tick-by-tick data for high-frequency analysis |

### Trading Skills

| Skill | Description |
|-------|-------------|
| `get_orders` | Retrieve pending orders |
| `get_positions` | Get open positions with metrics |
| `place_market_order` | Execute market buy/sell orders |
| `close_positions` | Close open positions |
| `update_sltp` | Modify stop loss and take profit |
| `get_history_orders` | Get historical orders |
| `get_history_deals` | Get executed deals history |

### Analysis Skills

| Skill | Description |
|-------|-------------|
| `calculate_margin` | Calculate margin required for a trade |
| `calculate_profit` | Calculate potential profit/loss |
| `calculate_max_volume` | Find maximum tradeable volume for given margin |
| `calculate_spread` | Get current spread and spread ratio |

## AI Agent Integration

### Getting Tool Definitions

Generate tool definitions compatible with OpenAI, Anthropic, and other AI frameworks:

```python
from mt5_agent_skills import get_registry

registry = get_registry()
tools = registry.get_tool_definitions()

# Use with OpenAI
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[...],
    tools=tools
)
```

### Executing Skills from Agent Responses

```python
import json

def handle_tool_call(tool_name: str, arguments: str) -> str:
    """Handle a tool call from an AI agent."""
    registry = get_registry()
    params = json.loads(arguments)
    result = registry.execute(tool_name, **params)
    return result.to_agent_response()
```

### Custom Skill Registration

```python
from mt5_agent_skills import BaseSkill, SkillInput, SkillResult, get_registry
from pydantic import Field

class MyCustomInput(SkillInput):
    symbol: str = Field(description="Trading symbol")
    threshold: float = Field(description="Alert threshold")

class MyCustomSkill(BaseSkill):
    @property
    def name(self) -> str:
        return "my_custom_skill"

    @property
    def description(self) -> str:
        return "A custom skill for specialized analysis"

    @property
    def category(self) -> str:
        return "custom"

    @property
    def input_model(self):
        return MyCustomInput

    def execute(self, **kwargs) -> SkillResult:
        # Your custom logic here
        return SkillResult(success=True, data={"result": "..."})

# Register the custom skill
registry = get_registry()
registry.register(MyCustomSkill())
```

## Skill Categories

```python
from mt5_agent_skills import get_registry

registry = get_registry()

# List all categories
categories = registry.get_categories()
# ['account', 'market_data', 'trading', 'analysis']

# Get skills by category
trading_skills = registry.list_skills_by_category("trading")
for skill in trading_skills:
    print(f"{skill.name}: {skill.description}")
```

## Error Handling

All skills return a `SkillResult` object:

```python
result = registry.execute("get_symbol_info", symbol="INVALID")

if result.success:
    print(result.data)
else:
    print(f"Error: {result.error}")
```

## Timeframes

Supported timeframes for OHLCV data:

- Minutes: `M1`, `M2`, `M3`, `M4`, `M5`, `M6`, `M10`, `M12`, `M15`, `M20`, `M30`
- Hours: `H1`, `H2`, `H3`, `H4`, `H6`, `H8`, `H12`
- Daily/Weekly/Monthly: `D1`, `W1`, `MN1`

## Development

```bash
# Clone the repository
git clone https://github.com/dceoy/mt5-agent-skills.git
cd mt5-agent-skills

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .

# Run type checking
mypy src/mt5_agent_skills
```

## License

This project is licensed under the AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## Related Projects

- [pdmt5](https://github.com/dceoy/pdmt5) - Pandas-based MetaTrader 5 data handler
- [MetaTrader5](https://pypi.org/project/MetaTrader5/) - Official MT5 Python package
