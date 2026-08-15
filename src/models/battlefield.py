from typing import Dict
from pydantic import BaseModel, Field

class Battlefield(BaseModel):
    name: str = Field(..., description="The mythic name of the terrain (e.g., AI Training Killing Fields)")
    description: str = Field(..., description="A description of the field's environment and stakes")
    rewards: str = Field(..., description="What characteristics or dimensions this battlefield rewards")
    suffers: str = Field(..., description="Who or what usually suffers on this terrain")
    dimension_weights: Dict[str, float] = Field(
        ..., 
        description="Weight multipliers for each scoring dimension (e.g., {'AI / GPU War Power': 2.0})"
    )
