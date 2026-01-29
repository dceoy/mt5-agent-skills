"""Analysis skills for MT5 Agent Skills.

This module provides skills for performing trading analysis calculations
including margin requirements, profit calculations, and spread analysis.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from mt5_agent_skills.client import get_client_manager
from mt5_agent_skills.core import BaseSkill, OrderSide, SkillInput, SkillResult


class CalculateMarginInput(SkillInput):
    """Input for calculating margin requirements."""

    symbol: str = Field(description="Symbol to calculate margin for (e.g., 'EURUSD')")
    volume: float = Field(gt=0, description="Trade volume in lots")
    order_side: OrderSide = Field(description="Order side: 'BUY' or 'SELL'")
    price: float | None = Field(
        default=None,
        description="Price to calculate at. If None, uses current market price.",
    )


class CalculateProfitInput(SkillInput):
    """Input for calculating profit."""

    symbol: str = Field(description="Symbol to calculate profit for (e.g., 'EURUSD')")
    volume: float = Field(gt=0, description="Trade volume in lots")
    order_side: OrderSide = Field(description="Order side: 'BUY' or 'SELL'")
    price_open: float = Field(description="Opening price")
    price_close: float = Field(description="Closing price")


class CalculateMaxVolumeInput(SkillInput):
    """Input for calculating maximum volume."""

    symbol: str = Field(description="Symbol to calculate volume for (e.g., 'EURUSD')")
    margin: float = Field(gt=0, description="Available margin amount")
    order_side: OrderSide = Field(description="Order side: 'BUY' or 'SELL'")


class CalculateSpreadInput(SkillInput):
    """Input for calculating spread."""

    symbol: str = Field(description="Symbol to calculate spread for (e.g., 'EURUSD')")


class CalculateMarginSkill(BaseSkill):
    """Skill to calculate margin requirements for a trade.

    Calculates the margin required to open a position of specified
    volume for a given symbol.
    """

    @property
    def name(self) -> str:
        return "calculate_margin"

    @property
    def description(self) -> str:
        return (
            "Calculate the margin requirement for opening a position with specified "
            "symbol, volume, and order side. Useful for risk management."
        )

    @property
    def category(self) -> str:
        return "analysis"

    @property
    def input_model(self) -> type[SkillInput]:
        return CalculateMarginInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to calculate margin.

        Args:
            symbol: Symbol to calculate for.
            volume: Trade volume in lots.
            order_side: 'BUY' or 'SELL'.
            price: Optional price (uses market price if not provided).

        Returns:
            SkillResult with margin calculation.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            volume = kwargs["volume"]
            order_side = kwargs["order_side"]
            price = kwargs.get("price")

            if isinstance(order_side, OrderSide):
                order_side = order_side.value

            margin = client.calculate_minimum_order_margin(
                symbol=symbol,
                volume=volume,
                order_side=order_side,
            )

            if margin is None:
                return SkillResult(
                    success=False,
                    error=f"Could not calculate margin for {symbol}",
                )

            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "volume": volume,
                    "order_side": order_side,
                    "required_margin": margin,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class CalculateProfitSkill(BaseSkill):
    """Skill to calculate potential profit for a trade.

    Calculates the profit/loss for a hypothetical trade given
    entry and exit prices.
    """

    @property
    def name(self) -> str:
        return "calculate_profit"

    @property
    def description(self) -> str:
        return (
            "Calculate the potential profit or loss for a trade given the symbol, "
            "volume, order side, and entry/exit prices."
        )

    @property
    def category(self) -> str:
        return "analysis"

    @property
    def input_model(self) -> type[SkillInput]:
        return CalculateProfitInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to calculate profit.

        Args:
            symbol: Symbol to calculate for.
            volume: Trade volume in lots.
            order_side: 'BUY' or 'SELL'.
            price_open: Entry price.
            price_close: Exit price.

        Returns:
            SkillResult with profit calculation.
        """
        try:
            import MetaTrader5 as mt5

            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            volume = kwargs["volume"]
            order_side = kwargs["order_side"]
            price_open = kwargs["price_open"]
            price_close = kwargs["price_close"]

            if isinstance(order_side, OrderSide):
                order_side = order_side.value

            action = mt5.ORDER_TYPE_BUY if order_side == "BUY" else mt5.ORDER_TYPE_SELL

            profit = client.order_calc_profit(
                action=action,
                symbol=symbol,
                volume=volume,
                price_open=price_open,
                price_close=price_close,
            )

            if profit is None:
                return SkillResult(
                    success=False,
                    error=f"Could not calculate profit for {symbol}",
                )

            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "volume": volume,
                    "order_side": order_side,
                    "price_open": price_open,
                    "price_close": price_close,
                    "profit": profit,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class CalculateMaxVolumeSkill(BaseSkill):
    """Skill to calculate maximum tradeable volume for given margin.

    Calculates the maximum position size that can be opened with
    a specified margin amount.
    """

    @property
    def name(self) -> str:
        return "calculate_max_volume"

    @property
    def description(self) -> str:
        return (
            "Calculate the maximum trade volume (lot size) that can be opened "
            "with a given margin amount for a specified symbol and order side."
        )

    @property
    def category(self) -> str:
        return "analysis"

    @property
    def input_model(self) -> type[SkillInput]:
        return CalculateMaxVolumeInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to calculate max volume.

        Args:
            symbol: Symbol to calculate for.
            margin: Available margin amount.
            order_side: 'BUY' or 'SELL'.

        Returns:
            SkillResult with maximum volume calculation.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            margin = kwargs["margin"]
            order_side = kwargs["order_side"]

            if isinstance(order_side, OrderSide):
                order_side = order_side.value

            max_volume = client.calculate_volume_by_margin(
                symbol=symbol,
                margin=margin,
                order_side=order_side,
            )

            if max_volume is None:
                return SkillResult(
                    success=False,
                    error=f"Could not calculate max volume for {symbol}",
                )

            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "available_margin": margin,
                    "order_side": order_side,
                    "max_volume": max_volume,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class CalculateSpreadSkill(BaseSkill):
    """Skill to calculate spread for a symbol.

    Calculates the current spread and spread ratio for a symbol.
    """

    @property
    def name(self) -> str:
        return "calculate_spread"

    @property
    def description(self) -> str:
        return (
            "Calculate the current spread (difference between bid and ask prices) "
            "and spread ratio for a symbol. Useful for evaluating trading costs."
        )

    @property
    def category(self) -> str:
        return "analysis"

    @property
    def input_model(self) -> type[SkillInput]:
        return CalculateSpreadInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to calculate spread.

        Args:
            symbol: Symbol to calculate spread for.

        Returns:
            SkillResult with spread calculation.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]

            spread_ratio = client.calculate_spread_ratio(symbol=symbol)

            tick = client.symbol_info_tick(symbol=symbol)
            if tick is None:
                return SkillResult(
                    success=False,
                    error=f"Could not get tick data for {symbol}",
                )

            spread_points = tick.ask - tick.bid

            symbol_info = client.symbol_info(symbol=symbol)
            if symbol_info is None:
                return SkillResult(
                    success=False,
                    error=f"Could not get symbol info for {symbol}",
                )

            spread_pips = spread_points / symbol_info.point

            return SkillResult(
                success=True,
                data={
                    "symbol": symbol,
                    "bid": tick.bid,
                    "ask": tick.ask,
                    "spread_points": spread_points,
                    "spread_pips": spread_pips,
                    "spread_ratio": spread_ratio,
                },
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
