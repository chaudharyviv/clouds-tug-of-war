from src.agents.base import BaseAgent
from src.models.battlefield import Battlefield, COMEBACK_MULTIPLIER
from src.models.battle import ResearchNotes, BattleResult, DimensionScorecard
from src.models.combatant import Champion
from typing import Dict, List
from pydantic import BaseModel, Field
import json

# Tuning constants for the deterministic layers on top of the LLM's raw
# per-dimension scores. These control how often Tactical Advantage / Second
# Wind can actually swing a fight — kept as named constants so they can be
# playtested and adjusted without touching the scoring logic itself.
TACTICAL_BONUS_SCALE = 0.15  # max +15 points at 100% tactical relevance
SECOND_WIND_BASE_SWING = 20.0  # max base swing at 100% relevance, medium comeback profile
SECOND_WIND_UNDERDOG_CAP = 1.5  # underdog factor never exceeds this multiplier


class RawScores(BaseModel):
    """Temporary structured container for parsing raw LLM dimension scores."""
    scores_a: Dict[str, float]
    scores_b: Dict[str, float]
    decisive_blows: List[str]
    best_capability_index_a: int = Field(
        0, description="0-based index into Combatant A's capabilities list: their single "
        "strongest capability specifically relative to this battlefield, not just overall."
    )
    best_capability_index_b: int = Field(
        0, description="0-based index into Combatant B's capabilities list: their single "
        "strongest capability specifically relative to this battlefield, not just overall."
    )
    tactical_relevance_a: float = Field(
        0.0, description="0-100: how strongly Combatant A's best capability matches the "
        "battlefield's tactical rule."
    )
    tactical_relevance_b: float = Field(
        0.0, description="0-100: how strongly Combatant B's best capability matches the "
        "battlefield's tactical rule."
    )


class SecondWindPick(BaseModel):
    """Battlefield-aware selection of a capability for Second Wind comeback."""
    fact: str = Field(..., description="The exact capability chosen (must match original list)")
    reason: str = Field(..., description="One short sentence: why this capability matters on this battlefield")
    relevance: float = Field(
        50.0, description="0-100: how strongly this capability matters on this specific battlefield"
    )


class FightEngine(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Fight Engine",
            role="Referee and dynamic combat scorer",
            personality="Ruthless referee, hyper-logical, objective, unswayed by theatricality. You evaluate the raw physics of cloud architecture.",
            temperature=0.15
        )

    def _pick_second_wind_fact(
        self,
        loser_name: str,
        losing_notes: ResearchNotes,
        battlefield: Battlefield,
    ) -> tuple[str, str, float]:
        """
        Choose the single most battlefield-relevant real capability
        for the losing side's Second Wind. Falls back safely.
        """
        if not losing_notes.capabilities:
            return (
                "A desperate attempt to fall back on residual operational resilience.",
                "No strong researched capability was available.",
                0.0
            )

        # Cheap path: only one capability → use it
        if len(losing_notes.capabilities) == 1:
            return losing_notes.capabilities[0], "Only researched capability available.", 50.0

        prompt = (
            f"Combatant '{loser_name}' is losing on battlefield '{battlefield.name}'.\n"
            f"Battlefield rewards: {battlefield.rewards}\n"
            f"Battlefield punishes: {battlefield.suffers}\n\n"
            f"Their researched capabilities (you MUST pick one of these exactly):\n"
            + "\n".join(f"- {c}" for c in losing_notes.capabilities)
            + "\n\n"
            f"Pick the SINGLE capability that gives them the strongest realistic "
            f"counter-strike on THIS battlefield. Do not invent new facts.\n"
            f"Return JSON with:\n"
            f"- fact: the exact capability string you chose\n"
            f"- reason: one short sentence explaining why it matters here\n"
            f"- relevance: 0-100, how strongly this specific capability matters on THIS battlefield "
            f"(100 = decisive on this terrain, 0 = irrelevant)"
        )

        try:
            pick = self.query_llm_structured(prompt, SecondWindPick)
            # Safety: only accept if the model actually chose from the list
            if pick.fact in losing_notes.capabilities:
                return pick.fact, pick.reason, max(0.0, min(100.0, pick.relevance))
        except Exception:
            pass

        # Fallback: first capability (old behavior)
        return losing_notes.capabilities[0], "Fallback selection.", 50.0

    @staticmethod
    def _resolve_capability(notes: ResearchNotes, index: int) -> str:
        """Safely resolve an LLM-picked capability index against the researched list."""
        if 0 <= index < len(notes.capabilities):
            return notes.capabilities[index]
        return "No standout capability identified"

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
        # Ask LLM to evaluate baseline score from 0-100 only on the dimensions
        # THIS battlefield actually cares about — everything else is excluded
        # from the prompt and the aggregation below, not defaulted to weight 1.0.
        active_dims = battlefield.active_dimensions()
        dims_formatted = "\n".join(f"  {i+1}. {d}" for i, d in enumerate(active_dims))
        caps_a_formatted = "\n".join(f"  [{i}] {c}" for i, c in enumerate(notes_a.capabilities)) or "  (none listed)"
        caps_b_formatted = "\n".join(f"  [{i}] {c}" for i, c in enumerate(notes_b.capabilities)) or "  (none listed)"
        prompt = (
            f"You must grade a duel between two combatants on the battlefield '{battlefield.name}' ({battlefield.description}).\n\n"
            f"Combatant A: {champion_a.name}\n"
            f"Research Notes A: {notes_a.model_dump_json(indent=2)}\n\n"
            f"Combatant B: {champion_b.name}\n"
            f"Research Notes B: {notes_b.model_dump_json(indent=2)}\n\n"
            f"For each of the following dimensions — the ONLY ones this battlefield scores — provide an "
            f"objective score from 0 to 100 for both A and B:\n"
            f"{dims_formatted}\n\n"
            f"Provide your evaluation in a JSON structure containing 'scores_a' and 'scores_b' dicts mapping dimension names to float scores.\n"
            f"Also include 'decisive_blows' representing 2-3 technical reasons that swung key dimensions.\n\n"
            f"Tactical Advantage: this battlefield rewards '{battlefield.tactical_rule}'. From Combatant A's "
            f"capabilities:\n{caps_a_formatted}\n"
            f"pick the single index that best matches this rule as 'best_capability_index_a', and rate how "
            f"strongly it matches (0-100) as 'tactical_relevance_a'.\n"
            f"From Combatant B's capabilities:\n{caps_b_formatted}\n"
            f"pick the single index that best matches this rule as 'best_capability_index_b', and rate its "
            f"match strength (0-100) as 'tactical_relevance_b'."
        )

        raw_scores = self.query_llm_structured(prompt, RawScores)

        # Calculate weighted scores based on Battlefield dimension multipliers
        weighted_a: Dict[str, float] = {}
        weighted_b: Dict[str, float] = {}

        total_score_a = 0.0
        total_score_b = 0.0

        for dim, weight in active_dims.items():
            score_a = raw_scores.scores_a.get(dim, 50.0)
            score_b = raw_scores.scores_b.get(dim, 50.0)

            weighted_a[dim] = score_a * weight
            weighted_b[dim] = score_b * weight

            total_score_a += weighted_a[dim]
            total_score_b += weighted_b[dim]

        # Tactical Advantage: a deterministic bonus derived from the LLM's
        # relevance rating, not left to the LLM to decide the point value of.
        tactical_relevance_a = max(0.0, min(100.0, raw_scores.tactical_relevance_a))
        tactical_relevance_b = max(0.0, min(100.0, raw_scores.tactical_relevance_b))
        tactical_bonus_a = round(tactical_relevance_a * TACTICAL_BONUS_SCALE, 1)
        tactical_bonus_b = round(tactical_relevance_b * TACTICAL_BONUS_SCALE, 1)
        total_score_a += tactical_bonus_a
        total_score_b += tactical_bonus_b

        tactical_capability_a = self._resolve_capability(notes_a, raw_scores.best_capability_index_a)
        tactical_capability_b = self._resolve_capability(notes_b, raw_scores.best_capability_index_b)

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

        # Pick the most battlefield-relevant capability for the losing side's Second Wind
        second_wind_fact, second_wind_reason, second_wind_relevance = self._pick_second_wind_fact(
            loser_name, losing_notes, battlefield
        )

        # Second Wind impact = capability relevance x battlefield comeback profile x
        # underdog factor. A close fight lets the loser swing harder if they connect;
        # this replaces the old margin-derived formula, which ignored the actual
        # researched capability entirely.
        comeback_multiplier = COMEBACK_MULTIPLIER[battlefield.comeback_profile]
        winner_total = max(total_score_a, total_score_b)
        underdog_factor = min(1.0 + (margin / winner_total) * 0.5, SECOND_WIND_UNDERDOG_CAP) if winner_total > 0 else 1.0
        second_wind_impact = round(
            (second_wind_relevance / 100.0) * SECOND_WIND_BASE_SWING * comeback_multiplier * underdog_factor,
            1
        )

        scorecards = {
            champion_a.name: DimensionScorecard(scores=raw_scores.scores_a, weighted_scores=weighted_a),
            champion_b.name: DimensionScorecard(scores=raw_scores.scores_b, weighted_scores=weighted_b)
        }

        return BattleResult(
            winner_name=winner_name,
            loser_name=loser_name,
            margin=round(margin, 2),
            score_a=round(total_score_a, 2),
            score_b=round(total_score_b, 2),
            second_wind_triggered=False,
            second_wind_fact=second_wind_fact,
            second_wind_reason=second_wind_reason,
            second_wind_impact=second_wind_impact,
            decisive_blows=raw_scores.decisive_blows,
            scorecards=scorecards,
            tactical_capability_a=tactical_capability_a,
            tactical_bonus_a=tactical_bonus_a,
            tactical_capability_b=tactical_capability_b,
            tactical_bonus_b=tactical_bonus_b
        )
