"""Skill registry for MT5 Agent Skills.

This module provides a registry for discovering, managing, and executing
MT5 skills. It serves as the main interface for AI agents to interact
with the available skills.
"""

from __future__ import annotations

from typing import Any

from mt5_agent_skills.core import BaseSkill, SkillMetadata, SkillResult
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


class SkillRegistry:
    """Registry for MT5 agent skills.

    The registry provides a centralized way to:
    - Discover available skills
    - Get skill metadata for AI agent tool definitions
    - Execute skills by name with validated parameters

    Example:
        >>> registry = SkillRegistry()
        >>> # List all available skills
        >>> for skill in registry.list_skills():
        ...     print(f"{skill.name}: {skill.description}")
        ...
        >>> # Execute a skill
        >>> result = registry.execute("get_account_info")
        >>> print(result.to_agent_response())
    """

    def __init__(self) -> None:
        """Initialize the registry with all available skills."""
        self._skills: dict[str, BaseSkill] = {}
        self._register_default_skills()

    def _register_default_skills(self) -> None:
        """Register all default MT5 skills."""
        default_skills: list[BaseSkill] = [
            # Account skills
            GetAccountInfoSkill(),
            GetTerminalInfoSkill(),
            # Market data skills
            GetSymbolsSkill(),
            GetSymbolInfoSkill(),
            GetTickSkill(),
            GetLatestRatesSkill(),
            GetRatesRangeSkill(),
            GetLatestTicksSkill(),
            # Trading skills
            GetOrdersSkill(),
            GetPositionsSkill(),
            PlaceMarketOrderSkill(),
            ClosePositionsSkill(),
            UpdateSLTPSkill(),
            GetHistoryOrdersSkill(),
            GetHistoryDealsSkill(),
            # Analysis skills
            CalculateMarginSkill(),
            CalculateProfitSkill(),
            CalculateMaxVolumeSkill(),
            CalculateSpreadSkill(),
        ]

        for skill in default_skills:
            self.register(skill)

    def register(self, skill: BaseSkill) -> None:
        """Register a skill in the registry.

        Args:
            skill: The skill instance to register.

        Raises:
            ValueError: If a skill with the same name is already registered.
        """
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' is already registered")
        self._skills[skill.name] = skill

    def unregister(self, name: str) -> None:
        """Remove a skill from the registry.

        Args:
            name: The name of the skill to remove.

        Raises:
            KeyError: If the skill is not found.
        """
        if name not in self._skills:
            raise KeyError(f"Skill '{name}' not found in registry")
        del self._skills[name]

    def get(self, name: str) -> BaseSkill | None:
        """Get a skill by name.

        Args:
            name: The skill name.

        Returns:
            The skill instance if found, None otherwise.
        """
        return self._skills.get(name)

    def list_skills(self) -> list[SkillMetadata]:
        """List all registered skills with their metadata.

        Returns:
            List of SkillMetadata objects for all registered skills.
        """
        return [skill.get_metadata() for skill in self._skills.values()]

    def list_skills_by_category(self, category: str) -> list[SkillMetadata]:
        """List skills filtered by category.

        Args:
            category: The category to filter by.

        Returns:
            List of SkillMetadata for skills in the specified category.
        """
        return [
            skill.get_metadata()
            for skill in self._skills.values()
            if skill.category == category
        ]

    def get_categories(self) -> list[str]:
        """Get all unique skill categories.

        Returns:
            List of category names.
        """
        return list({skill.category for skill in self._skills.values()})

    def execute(self, name: str, **kwargs: Any) -> SkillResult:
        """Execute a skill by name with parameters.

        Args:
            name: The skill name to execute.
            **kwargs: Parameters to pass to the skill.

        Returns:
            SkillResult with execution outcome.
        """
        skill = self.get(name)
        if skill is None:
            return SkillResult(
                success=False, error=f"Skill '{name}' not found in registry"
            )
        return skill.validate_and_execute(**kwargs)

    def get_tool_definitions(self) -> list[dict[str, Any]]:
        """Generate tool definitions for AI agent frameworks.

        Returns a list of tool definitions in a format compatible with
        common AI agent frameworks (OpenAI, Anthropic, etc.).

        Returns:
            List of tool definition dictionaries.
        """
        tools = []
        for skill in self._skills.values():
            metadata = skill.get_metadata()
            tool = {
                "type": "function",
                "function": {
                    "name": metadata.name,
                    "description": metadata.description,
                    "parameters": metadata.parameters_schema,
                },
            }
            tools.append(tool)
        return tools

    def get_skill_names(self) -> list[str]:
        """Get list of all registered skill names.

        Returns:
            List of skill names.
        """
        return list(self._skills.keys())


# Global registry instance
_registry: SkillRegistry | None = None


def get_registry() -> SkillRegistry:
    """Get the global skill registry instance.

    Returns:
        The singleton SkillRegistry instance.
    """
    global _registry
    if _registry is None:
        _registry = SkillRegistry()
    return _registry
