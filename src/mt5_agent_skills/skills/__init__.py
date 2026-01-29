"""MT5 Agent Skills package.

This package contains all available skills organized by category.
"""

from mt5_agent_skills.skills.account import (
    GetAccountInfoSkill,
    GetTerminalInfoSkill,
)
from mt5_agent_skills.skills.analysis import (
    CalculateMarginSkill,
    CalculateMaxVolumeSkill,
    CalculateProfitSkill,
    CalculateSpreadSkill,
)
from mt5_agent_skills.skills.market_data import (
    GetLatestRatesSkill,
    GetLatestTicksSkill,
    GetRatesRangeSkill,
    GetSymbolInfoSkill,
    GetSymbolsSkill,
    GetTickSkill,
)
from mt5_agent_skills.skills.trading import (
    ClosePositionsSkill,
    GetHistoryDealsSkill,
    GetHistoryOrdersSkill,
    GetOrdersSkill,
    GetPositionsSkill,
    PlaceMarketOrderSkill,
    UpdateSLTPSkill,
)

__all__ = [
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
