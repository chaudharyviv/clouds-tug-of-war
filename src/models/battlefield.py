from typing import Dict, Literal
from pydantic import BaseModel, Field

ComebackProfile = Literal["low", "medium", "high", "very_high"]

# How strongly a battlefield's Second Wind swing scales with capability
# relevance. Edge/ambush terrain rewards a well-placed counter-strike far
# more than a cost fight, where the numbers are harder to argue with.
COMEBACK_MULTIPLIER: Dict[ComebackProfile, float] = {
    "low": 0.5,
    "medium": 1.0,
    "high": 1.5,
    "very_high": 2.0,
}

class Battlefield(BaseModel):
    name: str = Field(..., description="The mythic name of the terrain (e.g., AI Training Killing Fields)")
    description: str = Field(..., description="A description of the field's environment and stakes")
    rewards: str = Field(..., description="What characteristics or dimensions this battlefield rewards")
    suffers: str = Field(..., description="Who or what usually suffers on this terrain")

    primary_dimensions: Dict[str, float] = Field(
        ..., description="2-3 dimensions this battlefield is actually about. Weight 2.0-3.0."
    )
    secondary_dimensions: Dict[str, float] = Field(
        default_factory=dict, description="1-2 dimensions that matter some. Weight 1.0-1.5."
    )
    # Any dimension not listed in primary_dimensions or secondary_dimensions is
    # not scored at all on this battlefield — it's excluded from the LLM prompt
    # and the aggregation, not defaulted to a weight of 1.0.

    tactical_rule: str = Field(
        ..., description="What kind of researched capability earns a Tactical Advantage here."
    )
    comeback_profile: ComebackProfile = Field(
        default="medium", description="How large a Second Wind swing this battlefield allows."
    )

    def active_dimensions(self) -> Dict[str, float]:
        """Every scored dimension on this battlefield, secondary weights overridden by primary."""
        return {**self.secondary_dimensions, **self.primary_dimensions}
