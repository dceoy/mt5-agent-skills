"""MT5 Agent Skills - Agent Skills for MetaTrader 5.

This package provides a set of skills for AI agents to interact with
MetaTrader 5 via the pdmt5 library. Skills are organized into categories:

- **account**: Account and terminal information
- **market_data**: Symbols, rates, ticks, and market data
- **trading**: Orders, positions, and trade execution
- **analysis**: Margin, profit, and spread calculations

Quick Start:
    >>> from mt5_agent_skills import get_registry, get_client_manager
    >>>
    >>> # Configure and connect to MT5
    >>> manager = get_client_manager()
    >>> manager.configure(login=12345, password="pwd", server="Server")
    >>> manager.connect()
    >>>
    >>> # Get the skill registry
    >>> registry = get_registry()
    >>>
    >>> # Execute a skill
    >>> result = registry.execute("get_account_info")
    >>> print(result.to_agent_response())
    >>>
    >>> # List available skills
    >>> for skill in registry.list_skills():
    ...     print(f"{skill.name}: {skill.description}")

Context Manager Usage:
    >>> from mt5_agent_skills import mt5_connection, get_registry
    >>>
    >>> with mt5_connection(12345, "password", "Server"):
    ...     registry = get_registry()
    ...     result = registry.execute("get_symbols", group="*USD*")
    ...     print(result.data)
"""

__version__ = "0.1.0"

from mt5_agent_skills.client import (
    Mt5ClientManager,
    get_client_manager,
    mt5_connection,
)
from mt5_agent_skills.core import (
    BaseSkill,
    OrderSide,
    SkillInput,
    SkillMetadata,
    SkillResult,
    Timeframe,
)
from mt5_agent_skills.registry import SkillRegistry, get_registry
from mt5_agent_skills.skills import (
    CalculateMarginSkill,
    CalculateMaxVolumeSkill,
    CalculateProfitSkill,
    CalculateSpreadSkill,
    ClosePositionsSkill,
    GetAccountInfoSkill,
    GetHistoryDealsSkill,
    GetHistoryOrdersSkill,
    GetLatestRatesSkill,
    GetLatestTicksSkill,
    GetOrdersSkill,
    GetPositionsSkill,
    GetRatesRangeSkill,
    GetSymbolInfoSkill,
    GetSymbolsSkill,
    GetTerminalInfoSkill,
    GetTickSkill,
    PlaceMarketOrderSkill,
    UpdateSLTPSkill,
)

__all__ = [
    # Version
    "__version__",
    # Client management
    "Mt5ClientManager",
    "get_client_manager",
    "mt5_connection",
    # Core classes
    "BaseSkill",
    "OrderSide",
    "SkillInput",
    "SkillMetadata",
    "SkillResult",
    "Timeframe",
    # Registry
    "SkillRegistry",
    "get_registry",
    # Account skills
    "GetAccountInfoSkill",
    "GetTerminalInfoSkill",
    # Market data skills
    "GetLatestRatesSkill",
    "GetLatestTicksSkill",
    "GetRatesRangeSkill",
    "GetSymbolInfoSkill",
    "GetSymbolsSkill",
    "GetTickSkill",
    # Trading skills
    "ClosePositionsSkill",
    "GetHistoryDealsSkill",
    "GetHistoryOrdersSkill",
    "GetOrdersSkill",
    "GetPositionsSkill",
    "PlaceMarketOrderSkill",
    "UpdateSLTPSkill",
    # Analysis skills
    "CalculateMarginSkill",
    "CalculateMaxVolumeSkill",
    "CalculateProfitSkill",
    "CalculateSpreadSkill",
]
