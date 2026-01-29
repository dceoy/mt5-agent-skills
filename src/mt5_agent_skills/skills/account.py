"""Account-related skills for MT5 Agent Skills.

This module provides skills for retrieving account and terminal information
from MetaTrader 5.
"""

from __future__ import annotations

from typing import Any

from mt5_agent_skills.client import get_client_manager
from mt5_agent_skills.core import BaseSkill, SkillInput, SkillResult


class EmptyInput(SkillInput):
    """Input model for skills that require no parameters."""

    pass


class GetAccountInfoSkill(BaseSkill):
    """Skill to retrieve MT5 account information.

    Returns account details including:
    - Account balance, equity, margin
    - Leverage and currency
    - Account type and trade mode
    - Profit and margin levels
    """

    @property
    def name(self) -> str:
        return "get_account_info"

    @property
    def description(self) -> str:
        return (
            "Retrieve detailed information about the connected MT5 trading account, "
            "including balance, equity, margin, leverage, and account type."
        )

    @property
    def category(self) -> str:
        return "account"

    @property
    def input_model(self) -> type[SkillInput]:
        return EmptyInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get account information.

        Returns:
            SkillResult with account information as a dictionary.
        """
        try:
            client = get_client_manager().get_client()
            account_info = client.account_info_as_dict()
            return SkillResult(success=True, data=account_info)
        except Exception as e:
            return SkillResult(success=False, error=str(e))


class GetTerminalInfoSkill(BaseSkill):
    """Skill to retrieve MT5 terminal information.

    Returns terminal details including:
    - Terminal version and build
    - Connection status
    - Trade permissions
    - Server information
    """

    @property
    def name(self) -> str:
        return "get_terminal_info"

    @property
    def description(self) -> str:
        return (
            "Retrieve information about the MT5 terminal, including version, "
            "build number, connection status, and trade permissions."
        )

    @property
    def category(self) -> str:
        return "account"

    @property
    def input_model(self) -> type[SkillInput]:
        return EmptyInput

    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill to get terminal information.

        Returns:
            SkillResult with terminal information as a dictionary.
        """
        try:
            client = get_client_manager().get_client()
            terminal_info = client.terminal_info()
            if terminal_info is None:
                return SkillResult(
                    success=False, error="Failed to retrieve terminal information"
                )
            return SkillResult(success=True, data=terminal_info._asdict())
        except Exception as e:
            return SkillResult(success=False, error=str(e))
