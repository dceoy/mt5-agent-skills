"""Core module for MT5 Agent Skills.

This module provides the base classes, configuration models, and skill infrastructure
for building AI agent skills that interact with MetaTrader 5 via pdmt5.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field


class Timeframe(str, Enum):
    """Supported MT5 timeframes."""

    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"
    M5 = "M5"
    M6 = "M6"
    M10 = "M10"
    M12 = "M12"
    M15 = "M15"
    M20 = "M20"
    M30 = "M30"
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"
    H4 = "H4"
    H6 = "H6"
    H8 = "H8"
    H12 = "H12"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"


class OrderSide(str, Enum):
    """Order side for trading operations."""

    BUY = "BUY"
    SELL = "SELL"


class SkillResult(BaseModel):
    """Base model for skill execution results."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool = Field(description="Whether the skill execution succeeded")
    data: Any | None = Field(default=None, description="Result data if successful")
    error: str | None = Field(default=None, description="Error message if failed")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Execution timestamp"
    )

    def to_agent_response(self) -> str:
        """Convert result to a string format suitable for AI agent consumption."""
        if self.success:
            if isinstance(self.data, dict):
                return json.dumps(self.data, indent=2, default=str)
            if isinstance(self.data, list):
                return json.dumps(self.data, indent=2, default=str)
            return str(self.data)
        return f"Error: {self.error}"


class SkillInput(BaseModel):
    """Base model for skill inputs."""

    model_config = ConfigDict(extra="forbid")


class SkillMetadata(BaseModel):
    """Metadata for a skill."""

    name: str = Field(description="Unique skill name")
    description: str = Field(description="Human-readable description of the skill")
    category: str = Field(description="Skill category (e.g., 'market_data', 'trading')")
    parameters_schema: dict[str, Any] = Field(
        description="JSON schema for skill parameters"
    )
    returns_schema: dict[str, Any] = Field(description="JSON schema for return value")


InputT = TypeVar("InputT", bound=SkillInput)


class BaseSkill(ABC):
    """Abstract base class for all MT5 agent skills.

    Skills are individual capabilities that AI agents can use to interact
    with MetaTrader 5. Each skill has:
    - A unique name
    - Input validation via Pydantic models
    - Standardized output format
    - Metadata for agent discovery
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the skill."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description of what the skill does."""

    @property
    @abstractmethod
    def category(self) -> str:
        """Category grouping for the skill."""

    @property
    @abstractmethod
    def input_model(self) -> type[SkillInput]:
        """Pydantic model class for validating inputs."""

    @abstractmethod
    def execute(self, **kwargs: Any) -> SkillResult:
        """Execute the skill with the given parameters.

        Args:
            **kwargs: Skill-specific parameters that will be validated
                     against the input_model.

        Returns:
            SkillResult containing success status and data or error.
        """

    def get_metadata(self) -> SkillMetadata:
        """Get metadata about this skill for agent discovery."""
        return SkillMetadata(
            name=self.name,
            description=self.description,
            category=self.category,
            parameters_schema=self.input_model.model_json_schema(),
            returns_schema=SkillResult.model_json_schema(),
        )

    def validate_and_execute(self, **kwargs: Any) -> SkillResult:
        """Validate inputs and execute the skill.

        This method provides automatic input validation before execution.

        Args:
            **kwargs: Skill-specific parameters.

        Returns:
            SkillResult containing success status and data or error.
        """
        try:
            validated_input = self.input_model(**kwargs)
            return self.execute(**validated_input.model_dump())
        except Exception as e:
            return SkillResult(success=False, error=str(e))
