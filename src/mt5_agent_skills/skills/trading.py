"""Trading skills for MT5 Agent Skills.

This module provides skills for executing trades and managing positions
in MetaTrader 5.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from mt5_agent_skills.client import get_client_manager
from mt5_agent_skills.core import BaseSkill, OrderSide, SkillInput, SkillResult


class EmptyInput(SkillInput):
    """Input model for skills that require no parameters."""

    pass


class SymbolInput(SkillInput):
    """Input model for skills that only require a symbol."""

    symbol: str | None = Field(
        default=None,
        description="Symbol name to filter by (e.g., 'EURUSD'). If None, returns all.",
    )


class PlaceMarketOrderInput(SkillInput):
    """Input for placing a market order."""

    symbol: str = Field(description="Symbol to trade (e.g., 'EURUSD')")
    volume: float = Field(gt=0, description="Trade volume in lots")
    order_side: OrderSide = Field(description="Order side: 'BUY' or 'SELL'")
    sl: float | None = Field(default=None, description="Stop loss price")
    tp: float | None = Field(default=None, description="Take profit price")
    deviation: int = Field(default=20, ge=0, description="Maximum price deviation in points")
    comment: str = Field(default="", description="Order comment")
    magic: int = Field(default=0, ge=0, description="Magic number for order identification")
    dry_run: bool = Field(
        default=False,
        description="If True, only check the order without executing",
    )


class ClosePositionsInput(SkillInput):
    """Input for closing positions."""

    symbols: list[str] | None = Field(
        default=None,
        description="List of symbols to close positions for. If None, closes all positions.",
    )
    comment: str = Field(default="", description="Comment for close orders")
    deviation: int = Field(default=20, ge=0, description="Maximum price deviation in points")
    magic: int | None = Field(
        default=None,
        description="Only close positions with this magic number",
    )


class UpdateSLTPInput(SkillInput):
    """Input for updating stop loss and take profit."""

    symbol: str = Field(description="Symbol to update SLTP for")
    sl: float | None = Field(default=None, description="New stop loss price")
    tp: float | None = Field(default=None, description="New take profit price")


class HistoryInput(SkillInput):
    """Input for getting history data."""

    date_from: datetime | None = Field(
        default=None, description="Start date for history"
    )
    date_to: datetime | None = Field(default=None, description="End date for history")
    symbol: str | None = Field(default=None, description="Filter by symbol")


class GetOrdersSkill(BaseSkill):
    """Skill to retrieve pending orders.

    Returns information about all pending orders in the account.
    """

    @property
    def name(self) -> str:
        return "get_orders"

    @property
    def description(self) -> str:
        return (
            "Retrieve all pending orders in the MT5 account. "
            "Can be filtered by symbol."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return SymbolInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get pending orders.

        Args:
            symbol: Optional symbol to filter orders.

        Returns:
            SkillResult with orders data.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs.get("symbol")

            if symbol:
                orders_df = client.orders_get_as_df(symbol=symbol)
            else:
                orders_df = client.orders_get_as_df()

            if orders_df is None or orders_df.empty:
                return SkillResult(
                    success=True,
                    data={"count": 0, "orders": []},
                )

            orders_data = orders_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={"count": len(orders_data), "orders": orders_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetPositionsSkill(BaseSkill):
    """Skill to retrieve open positions.

    Returns information about all open positions with calculated metrics.
    """

    @property
    def name(self) -> str:
        return "get_positions"

    @property
    def description(self) -> str:
        return (
            "Retrieve all open positions in the MT5 account with calculated metrics "
            "including unrealized profit/loss. Can be filtered by symbol."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return SymbolInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get open positions.

        Args:
            symbol: Optional symbol to filter positions.

        Returns:
            SkillResult with positions data.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs.get("symbol")

            if symbol:
                positions_df = client.fetch_positions_with_metrics_as_df(symbols=[symbol])
            else:
                positions_df = client.fetch_positions_with_metrics_as_df()

            if positions_df is None or positions_df.empty:
                return SkillResult(
                    success=True,
                    data={"count": 0, "positions": []},
                )

            positions_data = positions_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={"count": len(positions_data), "positions": positions_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class PlaceMarketOrderSkill(BaseSkill):
    """Skill to place a market order.

    Places a market buy or sell order with optional stop loss and take profit.
    Supports dry run mode for order validation without execution.
    """

    @property
    def name(self) -> str:
        return "place_market_order"

    @property
    def description(self) -> str:
        return (
            "Place a market order (buy or sell) for a specified symbol and volume. "
            "Supports optional stop loss, take profit, and dry run mode for validation."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return PlaceMarketOrderInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to place a market order.

        Args:
            symbol: Symbol to trade.
            volume: Trade volume in lots.
            order_side: 'BUY' or 'SELL'.
            sl: Optional stop loss price.
            tp: Optional take profit price.
            deviation: Maximum price deviation.
            comment: Order comment.
            magic: Magic number.
            dry_run: If True, only validate without executing.

        Returns:
            SkillResult with order result.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            volume = kwargs["volume"]
            order_side = kwargs["order_side"]

            if isinstance(order_side, OrderSide):
                order_side = order_side.value

            sl = kwargs.get("sl")
            tp = kwargs.get("tp")
            deviation = kwargs.get("deviation", 20)
            comment = kwargs.get("comment", "")
            magic = kwargs.get("magic", 0)
            dry_run = kwargs.get("dry_run", False)

            result = client.place_market_order(
                symbol=symbol,
                volume=volume,
                order_side=order_side,
                sl=sl,
                tp=tp,
                deviation=deviation,
                comment=comment,
                magic=magic,
                dry_run=dry_run,
            )

            if result is None:
                return SkillResult(
                    success=False,
                    error="Order placement returned no result",
                )

            result_dict = {
                "retcode": result.retcode,
                "deal": result.deal,
                "order": result.order,
                "volume": result.volume,
                "price": result.price,
                "bid": result.bid,
                "ask": result.ask,
                "comment": result.comment,
                "request_id": result.request_id,
            }

            success = result.retcode == 10009  # TRADE_RETCODE_DONE

            return SkillResult(
                success=success,
                data=result_dict,
                error=None if success else f"Order failed with retcode {result.retcode}",
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class ClosePositionsSkill(BaseSkill):
    """Skill to close open positions.

    Closes positions for specified symbols or all positions.
    """

    @property
    def name(self) -> str:
        return "close_positions"

    @property
    def description(self) -> str:
        return (
            "Close open positions for specified symbols. If no symbols provided, "
            "closes all open positions. Can filter by magic number."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return ClosePositionsInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to close positions.

        Args:
            symbols: List of symbols to close. If None, closes all.
            comment: Comment for close orders.
            deviation: Maximum price deviation.
            magic: Optional magic number filter.

        Returns:
            SkillResult with close results.
        """
        try:
            client = get_client_manager().get_client()
            symbols = kwargs.get("symbols")
            comment = kwargs.get("comment", "")
            deviation = kwargs.get("deviation", 20)
            magic = kwargs.get("magic")

            close_kwargs: dict[str, Any] = {
                "comment": comment,
                "deviation": deviation,
            }
            if symbols:
                close_kwargs["symbols"] = symbols
            if magic is not None:
                close_kwargs["magic"] = magic

            results = client.close_open_positions(**close_kwargs)

            if not results:
                return SkillResult(
                    success=True,
                    data={"closed_count": 0, "results": []},
                )

            results_data = []
            for r in results:
                results_data.append({
                    "retcode": r.retcode,
                    "deal": r.deal,
                    "order": r.order,
                    "volume": r.volume,
                    "price": r.price,
                    "comment": r.comment,
                })

            return SkillResult(
                success=True,
                data={"closed_count": len(results_data), "results": results_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class UpdateSLTPSkill(BaseSkill):
    """Skill to update stop loss and take profit for positions.

    Modifies the SL/TP levels for open positions of a specified symbol.
    """

    @property
    def name(self) -> str:
        return "update_sltp"

    @property
    def description(self) -> str:
        return (
            "Update stop loss and/or take profit levels for open positions "
            "of a specified symbol."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return UpdateSLTPInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to update SLTP.

        Args:
            symbol: Symbol to update SLTP for.
            sl: New stop loss price (None to leave unchanged).
            tp: New take profit price (None to leave unchanged).

        Returns:
            SkillResult with update results.
        """
        try:
            client = get_client_manager().get_client()
            symbol = kwargs["symbol"]
            sl = kwargs.get("sl")
            tp = kwargs.get("tp")

            if sl is None and tp is None:
                return SkillResult(
                    success=False,
                    error="At least one of 'sl' or 'tp' must be provided",
                )

            results = client.update_sltp_for_open_positions(
                symbol=symbol,
                sl=sl,
                tp=tp,
            )

            if not results:
                return SkillResult(
                    success=True,
                    data={"updated_count": 0, "results": []},
                )

            results_data = []
            for r in results:
                results_data.append({
                    "retcode": r.retcode,
                    "deal": r.deal,
                    "order": r.order,
                    "comment": r.comment,
                })

            return SkillResult(
                success=True,
                data={"updated_count": len(results_data), "results": results_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetHistoryOrdersSkill(BaseSkill):
    """Skill to retrieve historical orders.

    Returns completed and cancelled orders from trading history.
    """

    @property
    def name(self) -> str:
        return "get_history_orders"

    @property
    def description(self) -> str:
        return (
            "Retrieve historical orders (completed and cancelled) from the account. "
            "Can be filtered by date range and symbol."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return HistoryInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get history orders.

        Args:
            date_from: Optional start date.
            date_to: Optional end date.
            symbol: Optional symbol filter.

        Returns:
            SkillResult with historical orders data.
        """
        try:
            client = get_client_manager().get_client()
            date_from = kwargs.get("date_from")
            date_to = kwargs.get("date_to")
            symbol = kwargs.get("symbol")

            history_kwargs: dict[str, Any] = {}
            if date_from:
                history_kwargs["date_from"] = date_from
            if date_to:
                history_kwargs["date_to"] = date_to
            if symbol:
                history_kwargs["symbol"] = symbol

            orders_df = client.history_orders_get_as_df(**history_kwargs)

            if orders_df is None or orders_df.empty:
                return SkillResult(
                    success=True,
                    data={"count": 0, "orders": []},
                )

            orders_data = orders_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={"count": len(orders_data), "orders": orders_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetHistoryDealsSkill(BaseSkill):
    """Skill to retrieve historical deals.

    Returns executed deals from trading history.
    """

    @property
    def name(self) -> str:
        return "get_history_deals"

    @property
    def description(self) -> str:
        return (
            "Retrieve historical deals (executed trades) from the account. "
            "Can be filtered by date range and symbol."
        )

    @property
    def category(self) -> str:
        return "trading"

    @property
    def input_model(self) -> type[SkillInput]:
        return HistoryInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get history deals.

        Args:
            date_from: Optional start date.
            date_to: Optional end date.
            symbol: Optional symbol filter.

        Returns:
            SkillResult with historical deals data.
        """
        try:
            client = get_client_manager().get_client()
            date_from = kwargs.get("date_from")
            date_to = kwargs.get("date_to")
            symbol = kwargs.get("symbol")

            history_kwargs: dict[str, Any] = {}
            if date_from:
                history_kwargs["date_from"] = date_from
            if date_to:
                history_kwargs["date_to"] = date_to
            if symbol:
                history_kwargs["symbol"] = symbol

            deals_df = client.history_deals_get_as_df(**history_kwargs)

            if deals_df is None or deals_df.empty:
                return SkillResult(
                    success=True,
                    data={"count": 0, "deals": []},
                )

            deals_data = deals_df.to_dict(orient="records")
            return SkillResult(
                success=True,
                data={"count": len(deals_data), "deals": deals_data},
            )
        except Exception as e:
            return SkillResult(success=False, error=str(e))
