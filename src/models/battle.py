from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ResearchNotes(BaseModel):
    capabilities: List[str] = Field(..., description="Real-world strengths, technical assets, features")
    limitations: List[str] = Field(..., description="Real-world limitations, bottlenecks, gaps")
    pricing_signal: str = Field(..., description="Unit economics, pricing model details")
    source_links: List[str] = Field(..., description="Source URLs retrieved from search")

class DimensionScorecard(BaseModel):
    # Mapping of Dimension Name -> Score (e.g. 0 to 100)
    scores: Dict[str, float] = Field(..., description="Evaluated scores per dimension for each combatant")
    weighted_scores: Dict[str, float] = Field(..., description="Scores after applying battlefield weights")

class BattleResult(BaseModel):
    winner_name: str = Field(..., description="Name of the surviving champion")
    loser_name: str = Field(..., description="Name of the defeated champion")
    margin: float = Field(..., description="Final score differential")
    second_wind_triggered: bool = Field(False, description="Whether Second Wind was activated by the losing side")
    second_wind_fact: Optional[str] = Field(None, description="The research fact used for the Second Wind comeback")
    second_wind_impact: Optional[float] = Field(None, description="The score adjustment from Second Wind")
    decisive_blows: List[str] = Field(..., description="Key dimensions or events that decided the outcome")
    scorecards: Dict[str, DimensionScorecard] = Field(..., description="Detailed score breakdowns per combatant")

class Chronicle(BaseModel):
    verdict: str = Field(..., description="Plain-text legible verdict line (e.g., AWS holds the field · CoreWeave falls)")
    saga: str = Field(..., description="Full bardic chronicle of the combat")

class CodexEntry(BaseModel):
    id: str = Field(..., description="Unique fight ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of the battle")
    combatant_a: str = Field(..., description="Champion A's name")
    combatant_b: str = Field(..., description="Champion B's name")
    battlefield: str = Field(..., description="Battlefield name")
    result: BattleResult = Field(..., description="Outcome details")
    chronicle: Chronicle = Field(..., description="Chronicle details")
