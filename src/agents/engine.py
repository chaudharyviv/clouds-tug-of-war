from src.agents.base import BaseAgent
from src.models.battlefield import Battlefield
from src.models.battle import ResearchNotes, BattleResult, DimensionScorecard
from src.models.combatant import Champion
from src.config import BATTLE_DIMENSIONS
from typing import Dict
from pydantic import BaseModel
import json

class FightEngine(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fight Engine",
            role="Referee and dynamic combat scorer",
            personality="Ruthless referee, hyper-logical, objective, unswayed by theatricality. You evaluate the raw physics of cloud architecture.",
            temperature=0.15
        )

    def score_battle(
        self, 
        champion_a: Champion, 
        notes_a: ResearchNotes, 
        champion_b: Champion, 
        notes_b: ResearchNotes, 
        battlefield: Battlefield
    ) -> BattleResult:
        """
        Evaluates dimension scores, applies battlefield weights, computes winner, 
        and extracts the potential Second Wind comeback fact for the losing side.
        """
        # Ask LLM to evaluate baseline score from 0-100 on ALL 10 dimensions for both combatants
        # based on their research notes and the battlefield conditions.
        prompt = (
            f"You must grade a duel between two combatants on the battlefield '{battlefield.name}' ({battlefield.description}).\n\n"
            f"Combatant A: {champion_a.name}\n"
            f"Research Notes A: {notes_a.model_dump_json(indent=2)}\n\n"
            f"Combatant B: {champion_b.name}\n"
            f"Research Notes B: {notes_b.model_dump_json(indent=2)}\n\n"
            f"For each of the following 10 dimensions, provide an objective score from 0 to 100 for both A and B:\n"
            f"{BATTLE_DIMENSIONS}\n\n"
            f"Provide your evaluation in a JSON structure containing 'scores_a' and 'scores_b' dicts mapping dimension names to float scores.\n"
            f"Also include 'decisive_blows' representing 2-3 technical reasons that swung key dimensions."
        )
        
        # Temporary structured container for parsing raw scores
        class RawScores(BaseModel):
            scores_a: Dict[str, float]
            scores_b: Dict[str, float]
            decisive_blows: list[str]

        raw_scores = self.query_llm_structured(prompt, RawScores)
        
        # Calculate weighted scores based on Battlefield dimension multipliers
        weighted_a: Dict[str, float] = {}
        weighted_b: Dict[str, float] = {}
        
        total_score_a = 0.0
        total_score_b = 0.0
        
        for dim in BATTLE_DIMENSIONS:
            weight = battlefield.dimension_weights.get(dim, 1.0)
            
            score_a = raw_scores.scores_a.get(dim, 50.0)
            score_b = raw_scores.scores_b.get(dim, 50.0)
            
            weighted_a[dim] = score_a * weight
            weighted_b[dim] = score_b * weight
            
            total_score_a += weighted_a[dim]
            total_score_b += weighted_b[dim]
            
        # Determine current winner & loser
        if total_score_a >= total_score_b:
            winner_name = champion_a.name
            loser_name = champion_b.name
            margin = total_score_a - total_score_b
            losing_notes = notes_b
        else:
            winner_name = champion_b.name
            loser_name = champion_a.name
            margin = total_score_b - total_score_a
            losing_notes = notes_a

        # Extract the strongest research point for the losing side's potential Second Wind
        # This will be stored for interactive activation in the UI.
        second_wind_fact = (
            losing_notes.capabilities[0] if losing_notes.capabilities 
            else "A desperate attempt to fallback on legacy backup protocols."
        )
        
        # Calculate dynamic Second Wind impact based on how relevant their best capability is to the battlefield
        second_wind_impact = round(margin * 0.4 + 5.0, 1)  # Usually narrows the margin, sometimes flips it if close

        scorecards = {
            champion_a.name: DimensionScorecard(scores=raw_scores.scores_a, weighted_scores=weighted_a),
            champion_b.name: DimensionScorecard(scores=raw_scores.scores_b, weighted_scores=weighted_b)
        }

        return BattleResult(
            winner_name=winner_name,
            loser_name=loser_name,
            margin=round(margin, 2),
            second_wind_triggered=False,
            second_wind_fact=second_wind_fact,
            second_wind_impact=second_wind_impact,
            decisive_blows=raw_scores.decisive_blows,
            scorecards=scorecards
        )
