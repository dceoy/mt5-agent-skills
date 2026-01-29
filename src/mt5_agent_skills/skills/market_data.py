"""Market data skills for MT5 Agent Skills.

This module provides skills for retrieving market data from MetaTrader 5,
including OHLCV rates, tick data, and symbol information.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from mt5_agent_skills.client import get_client_manager
from mt5_agent_skills.core import BaseSkill, SkillInput, SkillResult, Timeframe


class GetSymbolsInput(SkillInput):
    """Input for getting available symbols."""

    group: str | None = Field(
        default=None,
        description="Filter symbols by group pattern (e.g., '*USD*', 'Forex*')",
    )


class GetSymbolInfoInput(SkillInput):
    """Input for getting symbol information."""

    symbol: str = Field(description="Symbol name (e.g., 'EURUSD', 'GBPUSD')")


class GetTickInput(SkillInput):
    """Input for getting current tick data."""

    symbol: str = Field(description="Symbol name (e.g., 'EURUSD')")


class GetLatestRatesInput(SkillInput):
    """Input for getting latest OHLCV rates."""

    symbol: str = Field(description="Symbol name (e.g., 'EURUSD')")
    timeframe: Timeframe = Field(
        default=Timeframe.H1,
        description="Timeframe for the rates (e.g., 'M1', 'H1', 'D1')",
    )
    count: int = Field(
        default=100, ge=1, le=10000, description="Number of bars to retrieve"
    )


class GetRatesRangeInput(SkillInput):
    """Input for getting OHLCV rates for a date range."""

    symbol: str = Field(description="Symbol name (e.g., 'EURUSD')")
    timeframe: Timeframe = Field(
        default=Timeframe.H1,
        description="Timeframe for the rates (e.g., 'M1', 'H1', 'D1')",
    )
    date_from: datetime = Field(description="Start date/time for the range")
    date_to: datetime = Field(description="End date/time for the range")


class GetLatestTicksInput(SkillInput):
    """Input for getting latest tick data."""

    symbol: str = Field(description="Symbol name (e.g., 'EURUSD')")
    seconds: int = Field(
        default=60, ge=1, le=86400, description="Number of seconds of tick data"
    )


class GetSymbolsSkill(BaseSkill):
    """Skill to retrieve available trading symbols.

    Returns a list of available symbols, optionally filtered by group pattern.
    """

    @property
    def name(self) -> str:
        return "get_symbols"

    @property
    def description(self) -> str:
        return (
            "Retrieve a list of available trading symbols from MT5, "
            "optionally filtered by a group pattern (e.g., '*USD*' for USD pairs)."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetSymbolsInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get available symbols.

        Args:
            group: Optional filter pattern for symbols.

        Returns:
            SkillResult with list of symbol names.
        """
        try:
            client = get_client_manager().get_client()
            group = kwargs.get("group")
            if group:
                symbols = client.symbols_get(group=group)
            else:
                symbols = client.symbols_get()

            if symbols is None:
                return SkillResult(success=True, data=[])

            symbol_names = [s.name for s in symbols]
            return SkillResult(
                success=True,
                data={"count": len(symbol_names), "symbols": symbol_names},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetSymbolInfoSkill(BaseSkill):
    """Skill to retrieve detailed information about a symbol.

    Returns comprehensive symbol information including:
    - Bid/ask prices and spread
    - Trade specifications (lot size, tick size, etc.)
    - Trading hours and limitations
    - Margin requirements
    """

    @property
    def name(self) -> str:
        return "get_symbol_info"

    @property
    def description(self) -> str:
        return (
            "Retrieve detailed information about a trading symbol, including "
            "current prices, spread, lot specifications, and trading conditions."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetSymbolInfoInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get symbol information.

        Args:
            symbol: Symbol name to get information for.

        Returns:
            SkillResult with symbol information as a dictionary.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            symbol_info = client.symbol_info_as_dict(symbol=symbol)
            if symbol_info is None:
                return SkillResult(
                    success=False, error=f"Symbol '{symbol}' not found or not available"
                )
            return SkillResult(success=True, data=symbol_info)
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetTickSkill(BaseSkill):
    """Skill to retrieve the current tick for a symbol.

    Returns the latest tick data including:
    - Bid and ask prices
    - Last trade price
    - Volume
    - Timestamp
    """

    @property
    def name(self) -> str:
        return "get_tick"

    @property
    def description(self) -> str:
        return (
            "Retrieve the current tick (bid/ask prices, last price, volume) "
            "for a trading symbol."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetTickInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get current tick.

        Args:
            symbol: Symbol name to get tick for.

        Returns:
            SkillResult with tick data as a dictionary.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            tick = client.symbol_info_tick_as_dict(symbol=symbol)
            if tick is None:
                return SkillResult(
                    success=False,
                    error=f"Could not get tick for symbol '{symbol}'",
                )
            return SkillResult(success=True, data=tick)
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetLatestRatesSkill(BaseSkill):
    """Skill to retrieve latest OHLCV rates for a symbol.

    Returns historical price data as a list of OHLCV bars including:
    - Open, High, Low, Close prices
    - Tick volume and real volume
    - Bar timestamp
    """

    @property
    def name(self) -> str:
        return "get_latest_rates"

    @property
    def description(self) -> str:
        return (
            "Retrieve the latest OHLCV (Open, High, Low, Close, Volume) price bars "
            "for a symbol with a specified timeframe and count."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetLatestRatesInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get latest rates.

        Args:
            symbol: Symbol name.
            timeframe: Timeframe string (e.g., 'M1', 'H1', 'D1').
            count: Number of bars to retrieve.

        Returns:
            SkillResult with rates data as a list of dictionaries.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            timeframe = kwargs.get("timeframe", Timeframe.H1)
            count = kwargs.get("count", 100)

            if isinstance(timeframe, Timeframe):
                timeframe = timeframe.value

            rates_df = client.fetch_latest_rates_as_df(
                symbol=symbol,
                granularity=timeframe,
                count=count,
            )

            if rates_df is None or rates_df.empty:
                return SkillResult(
                    success=False,
                    error=f"No rates found for symbol '{symbol}'",
                )

            rates_df = rates_df.reset_index()
            rates_data = rates_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "count": len(rates_data),
                    "rates": rates_data,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetRatesRangeSkill(BaseSkill):
    """Skill to retrieve OHLCV rates for a specific date range.

    Returns historical price data between two dates.
    """

    @property
    def name(self) -> str:
        return "get_rates_range"

    @property
    def description(self) -> str:
        return (
            "Retrieve OHLCV price bars for a symbol within a specific date/time range. "
            "Useful for historical analysis of specific periods."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetRatesRangeInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get rates for a date range.

        Args:
            symbol: Symbol name.
            timeframe: Timeframe string.
            date_from: Start datetime.
            date_to: End datetime.

        Returns:
            SkillResult with rates data as a list of dictionaries.
        """
        try:
            import MetaTrader5 as mt5

            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            timeframe = kwargs.get("timeframe", Timeframe.H1)
            date_from = kwargs["date_from"]
            date_to = kwargs["date_to"]

            if isinstance(timeframe, Timeframe):
                timeframe = timeframe.value

            timeframe_map = {
                "M1": mt5.TIMEFRAME_M1,
                "M2": mt5.TIMEFRAME_M2,
                "M3": mt5.TIMEFRAME_M3,
                "M4": mt5.TIMEFRAME_M4,
                "M5": mt5.TIMEFRAME_M5,
                "M6": mt5.TIMEFRAME_M6,
                "M10": mt5.TIMEFRAME_M10,
                "M12": mt5.TIMEFRAME_M12,
                "M15": mt5.TIMEFRAME_M15,
                "M20": mt5.TIMEFRAME_M20,
                "M30": mt5.TIMEFRAME_M30,
                "H1": mt5.TIMEFRAME_H1,
                "H2": mt5.TIMEFRAME_H2,
                "H3": mt5.TIMEFRAME_H3,
                "H4": mt5.TIMEFRAME_H4,
                "H6": mt5.TIMEFRAME_H6,
                "H8": mt5.TIMEFRAME_H8,
                "H12": mt5.TIMEFRAME_H12,
                "D1": mt5.TIMEFRAME_D1,
                "W1": mt5.TIMEFRAME_W1,
                "MN1": mt5.TIMEFRAME_MN1,
            }

            mt5_timeframe = timeframe_map.get(timeframe, mt5.TIMEFRAME_H1)

            rates_df = client.copy_rates_range_as_df(
                symbol=symbol,
                timeframe=mt5_timeframe,
                date_from=date_from,
                date_to=date_to,
            )

            if rates_df is None or rates_df.empty:
                return SkillResult(
                    success=False,
                    error=f"No rates found for symbol '{symbol}' in the specified range",
                )

            rates_df = rates_df.reset_index()
            rates_data = rates_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "date_from": str(date_from),
                    "date_to": str(date_to),
                    "count": len(rates_data),
                    "rates": rates_data,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetLatestTicksSkill(BaseSkill):
    """Skill to retrieve recent tick data for a symbol.

    Returns tick-by-tick data for the specified number of seconds.
    """

    @property
    def name(self) -> str:
        return "get_latest_ticks"

    @property
    def description(self) -> str:
        return (
            "Retrieve tick-by-tick price data for a symbol for the last N seconds. "
            "Useful for high-frequency analysis and market microstructure study."
        )

    @property
    def category(self) -> str:
        return "market_data"

    @property
    def input_model(self) -> type[SkillInput]:
        return GetLatestTicksInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get latest ticks.

        Args:
            symbol: Symbol name.
            seconds: Number of seconds of tick data to retrieve.

        Returns:
            SkillResult with tick data as a list of dictionaries.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            seconds = kwargs.get("seconds", 60)

            ticks_df = client.fetch_latest_ticks_as_df(symbol=symbol, seconds=seconds)

            if ticks_df is None or ticks_df.empty:
                return SkillResult(
                    success=False,
                    error=f"No ticks found for symbol '{symbol}'",
                )

            ticks_df = ticks_df.reset_index()
            ticks_data = ticks_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "seconds": seconds,
                    "count": len(ticks_data),
                    "ticks": ticks_data,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
