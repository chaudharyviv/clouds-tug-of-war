# v3 Fight Engine — Concrete Design

Scope: the four changes you flagged as worth doing without a bigger rewrite:
1. Battlefields score only 3–5 active dimensions (rest = 0, not 1.0)
2. Tactical Advantage bonus, wired from the `best_capability_index_a/b` fields that already exist but are currently discarded
3. Second Wind rebuilt around capability relevance instead of `margin * 0.4 + 5`
4. Scoring math moved fully into deterministic Python; the LLM only supplies raw per-dimension scores + a relevance number

No code changes have been made. This is the concrete shape for review.

---

## 1. `Battlefield` model — [src/models/battlefield.py](../src/models/battlefield.py)

Current model has a single flat `dimension_weights: Dict[str, float]`, defaulted to `1.0` for anything unlisted (the bug you identified — `engine.py:132`).

```python
from typing import Dict, Literal
from pydantic import BaseModel, Field

ComebackProfile = Literal["low", "medium", "high", "very_high"]

COMEBACK_MULTIPLIER: Dict[ComebackProfile, float] = {
    "low": 0.5,
    "medium": 1.0,
    "high": 1.5,
    "very_high": 2.0,
}

class Battlefield(BaseModel):
    name: str
    description: str
    rewards: str
    suffers: str

    primary_dimensions: Dict[str, float] = Field(
        ..., description="2-3 dimensions this battlefield is actually about. Weight 2.0-3.0."
    )
    secondary_dimensions: Dict[str, float] = Field(
        default_factory=dict, description="1-2 dimensions that matter some. Weight 1.0-1.5."
    )
    # everything not in primary_dimensions or secondary_dimensions scores 0 — it's not computed,
    # not requested from the LLM, and doesn't appear in the scorecard.

    tactical_rule: str = Field(
        ..., description="One sentence: what kind of researched capability earns a Tactical Advantage here."
    )
    comeback_profile: ComebackProfile = "medium"

    def active_dimensions(self) -> Dict[str, float]:
        return {**self.secondary_dimensions, **self.primary_dimensions}
```

Dropping `dimension_weights` entirely (rather than keeping it alongside the new fields) avoids a second source of truth — nothing else in the repo reads it besides `engine.py`.

---

## 2. Battlefield data — [src/config.py](../src/config.py)

Same five battlefields, same flavor text, restructured. Example for two of them (the other three follow the same pattern from your doc):

```python
Battlefield(
    name="AI Training Killing Fields",
    description="...",
    rewards="GPU density, performance, specialized stacks",
    suffers="Generalist empires & pure edge",
    primary_dimensions={
        "AI / GPU War Power": 3.0,
        "Speed of Innovation / Specialization": 2.0,
    },
    secondary_dimensions={
        "Raw Scale & Gravity": 1.0,
    },
    tactical_rule="Specialized GPU/accelerator infrastructure earns a Tactical Advantage.",
    comeback_profile="high",
),
Battlefield(
    name="Cost Wasteland",
    description="...",
    rewards="Aggressive unit economics, low cost-per-token/VM",
    suffers="Premium gravity wells and high lock-in ecosystems",
    primary_dimensions={
        "Economic Blood Cost": 3.0,
    },
    secondary_dimensions={
        "Operational Simplicity": 1.5,
        "Lock-in vs Freedom": 1.0,
    },
    tactical_rule="Demonstrably lower sustainable unit economics earns a Tactical Advantage.",
    comeback_profile="low",
),
```

`Edge Ambush Terrain` gets `comeback_profile="very_high"`, `Lock-in Swamp` and `Sovereignty Fortress` get `"medium"` — matching your table.

---

## 3. `FightEngine.score_battle` — [src/agents/engine.py](../src/agents/engine.py)

### 3a. LLM contract shrinks and gets one new field

`RawScores` currently asks for full 10-dim scores on both sides plus two capability indices that are never used downstream (`engine.py:15-22` — dead weight, this is the "LLM decides the score, engine just multiplies" problem). New contract:

```python
class RawScores(BaseModel):
    scores_a: Dict[str, float]   # only battlefield.active_dimensions() keys, not all 10
    scores_b: Dict[str, float]
    decisive_blows: List[str]
    best_capability_index_a: int
    best_capability_index_b: int
    tactical_relevance_a: float = Field(..., description="0-100: how strongly A's best capability matches battlefield.tactical_rule")
    tactical_relevance_b: float = Field(..., description="0-100: same, for B")
```

Prompt changes:
- List only `battlefield.active_dimensions()` instead of all 10 `BATTLE_DIMENSIONS` (`engine.py:100,109`).
- Ask for `tactical_relevance_a/b` explicitly against `battlefield.tactical_rule`, scored against the *already-chosen* `best_capability_index`. This is the only new thing asked of the LLM — everything else (bonus size, winner, second wind size) moves to Python.

### 3b. Deterministic aggregation replaces `engine.py:131-141`

```python
total_score_a = 0.0
total_score_b = 0.0
weighted_a, weighted_b = {}, {}

for dim, weight in battlefield.active_dimensions().items():
    score_a = raw_scores.scores_a.get(dim, 50.0)
    score_b = raw_scores.scores_b.get(dim, 50.0)
    weighted_a[dim] = score_a * weight
    weighted_b[dim] = score_b * weight
    total_score_a += weighted_a[dim]
    total_score_b += weighted_b[dim]
```

No default-`1.0` fallthrough — a dimension the battlefield doesn't name simply isn't in the loop. This alone fixes the bug in your report.

### 3c. Tactical Advantage — deterministic bonus, not LLM-decided

```python
TACTICAL_BONUS_SCALE = 0.15  # tunable: max ~15 points at 100 relevance

tactical_bonus_a = raw_scores.tactical_relevance_a * TACTICAL_BONUS_SCALE
tactical_bonus_b = raw_scores.tactical_relevance_b * TACTICAL_BONUS_SCALE

total_score_a += tactical_bonus_a
total_score_b += tactical_bonus_b
```

The LLM says "how relevant is this real capability" (0-100, grounded in research — same Fidelity Law constraint already enforced for Second Wind picks via `_pick_second_wind_fact`). Python decides how many points that's worth. This is what makes `best_capability_index_a/b` finally do something (currently dead — computed at `engine.py:15-22`, never read after being set).

### 3d. Second Wind — replace `engine.py:161`

Current: `second_wind_impact = round(margin * 0.4 + 5.0, 1)` — a function of the score gap only, not of the losing side's actual capability. Replace with:

```python
# reuse _pick_second_wind_fact's LLM call, but also request a relevance score (0-100)
# instead of only fact+reason — extend SecondWindPick with `relevance: float`

comeback_multiplier = COMEBACK_MULTIPLIER[battlefield.comeback_profile]
underdog_factor = 1.0 + (margin / max(total_score_a, total_score_b)) * 0.5
# larger gap → losing side swings harder when they connect, capped below

second_wind_impact = round(
    (second_wind_relevance / 100.0) * 20.0 * comeback_multiplier * min(underdog_factor, 1.5),
    1
)
```

`20.0` is the max base swing at 100% relevance and multiplier 1.0; tune alongside `TACTICAL_BONUS_SCALE` during playtesting so `very_high` comeback battlefields can occasionally flip a moderate margin, `low` ones almost never can. This directly implements your "Second Wind Power = Capability Strength × Battlefield Relevance × Underdog Factor" formula (point 6 in your doc) instead of the margin-derived one.

### 3e. Second Wind application — already correct, no change needed

Initially assumed `second_wind_impact` needed to be auto-applied inside `score_battle`. It doesn't: the app already defers Second Wind to a manual "Activate Second Wind" button (`views.py:202`), which calls `ArenaOrchestrator.apply_second_wind` (`orchestrator.py:44-76`). That method already subtracts the impact from the margin and swaps `winner_name`/`loser_name` if the impact overtakes it — i.e. the win-flip logic your point 8 describes already exists, it just wasn't being fed a meaningful `second_wind_impact` value. Fixing 3d (below) is sufficient; `orchestrator.py` needs no changes.

---

## What doesn't change

- `BattleResult`, `DimensionScorecard`, `Chronicle`, `CodexEntry` schemas stay as-is — `scorecards` will just have fewer keys per combatant now (only active dimensions), which the Chronicler already consumes generically via `model_dump_json`.
- Chronicler/Weaver/Scout agents untouched.
- `_pick_second_wind_fact` keeps its structure, just gets a `relevance: float` field added to `SecondWindPick`.

## Deferred (not in this pass)

Everything else in your doc — Wounds as structured battle events, Battlefield Compatibility pre-fight preview, Ambush as a distinct outcome type, richer per-battlefield special rules beyond the single `tactical_rule` string. Those are additive on top of this foundation and don't require re-touching the scoring math again once this lands.

## Open tuning knobs to decide before implementing

- `TACTICAL_BONUS_SCALE` (suggested 0.15, i.e. max +15 at full relevance)
- Second Wind base swing constant (suggested 20.0)
- `underdog_factor` cap (suggested 1.5×)

These three constants are what actually control how often upsets happen — worth picking a few real fights to sanity-check against before hardcoding.
