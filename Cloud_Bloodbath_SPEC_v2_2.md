# CLOUD BLOODBATH

**Full Specification • Design • Architecture — v2**  
**Tone: Folklore × Thug-of-War × Absolute Cloud Carnage**  
**Domain: Multi-Faction War for the Cloud Realms**

---

> This is not a cloud comparison tool.  
> This is not a Gartner quadrant.  
> This is a mythic bloodsport where cloud empires, warbands, and guerrilla tribes fight for dominion over compute, data, and the future.

Any faction can fight any faction.  
The strong usually crush the weak.  
But the right battlefield — or the right desperate gambit — can turn the world upside down.

---

# 1. PRODUCT SPECIFICATION

## 1.1 Vision

**Cloud Bloodbath** is a small, high-creativity multi-agent system that stages savage, theatrical, and technically grounded wars between cloud factions and named players.

Users throw empires and upstarts into the arena. The system researches their real power, turns strengths into legendary weapons and weaknesses into curses, runs a dimension tug-of-war under battlefield rules, and writes a blood-soaked chronicle that declares who survives - clearly, not ambiguously.

**One-line pitch:**  
Real cloud architecture. Mythic violence. No survivors left unscarred.

## 1.2 Core Fantasy

The cloud is not a market. It is a collection of warring realms:

- **Hyperscalers** — The three ancient God-Empires. Infinite scale, deep magic, gravitational lock-in, and crushing tribute.
- **NeoClouds** — The new AI warbands. Lean, specialized, hungry, born for GPU bloodsport.
- **Sovereign / Regional Clouds** — Border kingdoms obsessed with data walls and national shields.
- **Distributed / Edge Tribes** — Guerrilla fighters living at the fringes. Fast locally, fragile in open war.
- **Private / On-Prem Empires** — The old fortress kingdoms still trying to hold their walls.

Power is asymmetric on purpose. Edge tribes rarely win open-field wars against God-Empires — and that is correct. They can still win ambushes, and they get one desperate swing before the end.

## 1.3 Target Users

- Engineers and operators tired of polite cloud comparisons
- People who want to watch NeoClouds try to assassinate Hyperscalers
- Portfolio reviewers who value creative technical systems built with restraint
- Anyone who enjoys watching sacred cows get stabbed with accurate knives

## 1.4 User Stories

1. As a warlord, I can throw any faction or named player against any other.
2. As a spectator, I can choose a battlefield that changes the laws of war.
3. As a realist, I still see real architectural strengths and weaknesses reflected in the carnage.
4. As a bloodthirsty fan, I get a full mythic chronicle with trash talk, a turning point, and a clear verdict.
5. As the underdog's fan, I get to watch them spend one real, earned comeback move before they fall.
6. As a returning fan, I can browse the Hall of Fame and the Graveyard of past cloud wars.

## 1.5 Functional Requirements

**Must Have**
- Multi-faction roster with named major players
- Any-vs-any matchups (1v1 for MVP; free-for-all and brackets in Phase 2 — see section 4.1)
- Battlefield selection that modifies scoring weights
- Research of real capabilities, economics, and limitations (single search tool)
- Mythic transformation (weapons, curses, epithets, battle styles)
- Dimension-based tug-of-war scoring
- Full blood-soaked battle chronicle
- **An unambiguous verdict** — winner, loser, and why, stated plainly before the flourish
- **One comeback move (Second Wind)** available to whoever is losing, spent once, grounded in a real research fact
- Visible technical backbone underneath the myth (Fidelity Law)

**Should Have**
- Pre-seeded classic grudge matches
- Theatrical odds shown before the fight
- Side-by-side "Myth vs Reality" view
- Rematch mode

**Phase 2 (scoped, see section 4.1)**
- Free-for-all / tournament brackets
- Hall of Fame / Graveyard persistence
- Multi-round campaigns

**Could Have**
- Generated fight posters
- Audio chronicle narration
- User-defined custom battlefields
- Seasonal "Cloud War" events

## 1.6 Non-Goals

- No TCO calculators presented as financial advice
- No compliance or governance engines
- No polite "it depends" advisor tone
- No enterprise decision-report formatting
- No forced equal win rates between weak and strong factions
- No sprawling agent pipeline or multi-search-provider infrastructure — this stays small on purpose

## 1.7 Success Criteria

A battle succeeds when:

1. A cloud engineer laughs and then admits the outcome is fair.
2. Power asymmetry feels real (Edge rarely topples AWS in open war).
3. The underdog still gets one real, earned moment before losing.
4. Weaknesses are turned into wounds, not politely hidden.
5. The verdict is legible at a glance — nobody has to guess who won.
6. **A non-engineer can tell who won in under 3 seconds.**
7. The technical truth remains recoverable behind the myth.

---

# 2. DESIGN

## 2.1 Design Principles

1. **Creativity is mandatory. Technical honesty is sacred.**
2. **Asymmetry is a feature.** The God-Empires should feel terrifying.
3. **Battlefields change destiny.** The same two fighters can produce different winners on different ground.
4. **The verdict is never ambiguous.** Fun lives in the myth, not in confusion about who won.
5. **The underdog gets one real swing.** Comebacks are earned from research, not free.
6. **The skeleton must stay visible.** Users can always inspect the real attributes behind the blood.
7. **Small pipeline, sharp execution.** Four agents done well beats six agents done thinly.

## 2.2 Faction & Player Mythology

### Core Factions

| Faction                    | Mythic Role                          | Real Mapping                          | Typical Fate in Open War      |
|----------------------------|--------------------------------------|---------------------------------------|-------------------------------|
| Hyperscalers               | The Three God-Empires                | AWS, Azure, GCP                       | Dominate most open battlefields |
| NeoClouds                  | AI War Bands / New Gods              | CoreWeave, Lambda, Crusoe, Voltage Park, etc. | Can upset Hyperscalers on AI ground |
| Sovereign / Regional       | Border Kingdoms & Data Walls         | Country/region clouds                 | Strong at home, weak abroad   |
| Distributed / Edge         | Guerrilla Tribes                     | Edge platforms & distributed systems  | Win ambushes, lose open wars  |
| Private / On-Prem Empires  | Old Fortress Kingdoms                | Traditional private cloud / on-prem   | Defensive, slowly eroding     |

### Named Champions (Examples)

- **AWS** — The First God, Lord of the Infinite Bill, Master of Gravitational Lock-in
- **Azure** — The Enterprise Titan, Wielder of Hybrid Pacts and Compliance Shields
- **GCP** — The Data & AI Oracle, Keeper of the Deep Analytics Flame
- **CoreWeave** — The GPU Berserker, Blade of the NeoCloud Rebellion
- **Lambda** — The Developer's Assassin
- **Crusoe** — The Energy Warlock (sustainable power as dark magic)
- Edge players — The Shadow Raiders, Masters of Local Ambush

Epithets, weapons, and flaws are generated from research notes, not invented freely.

## 2.3 Battle Dimensions (The Ropes)

1. Raw Scale & Gravity  
2. AI / GPU War Power  
3. Economic Blood Cost (pricing & unit economics)  
4. Operational Simplicity  
5. Service Depth & Ecosystem  
6. Lock-in vs Freedom  
7. Sovereign Control & Data Residency  
8. Edge / Locality Power  
9. Resilience & Global Reach  
10. Speed of Innovation / Specialization  

MVP scores a subset of these per battle (3–5 dimensions relevant to the chosen battlefield), not all ten every time — keeps the scorecard readable.

## 2.4 Battlefields (Laws of War Change Here)

| Battlefield                  | What it Rewards                              | Who Usually Suffers              |
|------------------------------|----------------------------------------------|----------------------------------|
| AI Training Killing Fields   | GPU density, performance, specialized stacks | Generalist empires & pure edge   |
| Cost Wasteland               | Aggressive unit economics                    | Premium gravity wells            |
| Lock-in Swamp                | Freedom and exit ability                     | Deep ecosystem empires           |
| Sovereignty Fortress         | Data residency and control                   | Global Hyperscalers              |
| Edge Ambush Terrain          | Locality and ultra-low latency               | Centralized cloud gods           |

MVP ships 5 battlefields (trimmed from 7 — Enterprise Hybrid Plains and Open Global Battlefield are post-MVP additions).

## 2.5 Agent Roster (The War Council) — simplified to four

| Agent                  | Responsibility                                                                 | Personality                     |
|------------------------|--------------------------------------------------------------------------------|---------------------------------|
| **War Scout**          | Runs the single search tool, produces plain research notes (capabilities, limitations, sources) per combatant | Cold, precise                   |
| **Myth Weaver**        | Turns research notes into weapons, curses, epithets, battle style              | Unhinged myth-maker             |
| **Fight Engine**       | Scores dimensions under battlefield rules, decides winner, resolves the Second Wind comeback if triggered | Ruthless referee                |
| **Blood Chronicler**   | Writes the full saga, states the verdict plainly, then delivers the theatrical flourish | Drunk bard + combat commentator |

This replaces the original six-agent council. Tug-of-War Engine and Body Counter merged into **Fight Engine**; the Arena Master's matchmaking role folded into the app's own UI logic rather than a separate agent — no agent needed to just read a form submission.

## 2.6 Power Asymmetry Rules

- Hyperscalers enter most open battles as heavy favorites.
- NeoClouds receive large bonuses on AI/GPU battlefields.
- Edge and Distributed factions receive large bonuses only on locality / ambush / sovereignty-edge terrains.
- The system must be willing to let the "weak" side get slaughtered when the battlefield demands it.
- Glorious death is still good content — which is what Second Wind is for.

## 2.7 The Second Wind (Cheat Code, With Rules)

The one comeback mechanic in the system. Simple by design:

- Triggers when a combatant is behind after scoring.
- Spends that combatant's single strongest **real** research point (from the Scout's notes, not invented) as one dramatic counter-strike beat in the chronicle.
- Available **once per battle**, to the losing side only.
- Does not overturn the final verdict on its own — it can narrow the margin or land a symbolic blow, but the Fidelity Law still governs whether it changes the outcome. Most of the time it doesn't; sometimes, on a close battlefield, it does.
- Logged separately in the scorecard so it's visible, not smuggled in as a hidden buff.

This is the one piece of "chaos" the system allows itself, and it's kept honest by tying it to something the War Scout actually found.

## 2.8 Fidelity Law

The Myth Weaver may be extreme.  
The Blood Chronicler may be unhinged.

Neither may invent capabilities that do not exist or erase well-known limitations.  
The War Scout's research notes remain the source of truth — including for what the Second Wind is allowed to draw on.

## 2.9 UI Direction — Gaming Page, Not a Form

Streamlit as the base, with CSS injection carrying the "gaming" feel — not a JS framework, not a game engine.

Core screen elements:

- **Battlefield banner** at top — the terrain, stated plainly, sets tone before the fight starts.
- **VS row** — two fighter panels with clipped diagonal edges (not plain rectangles), champion name in a display serif, stat bars restyled from `st.progress()`.
- **Verdict strip** — always visible, always literal ("AWS holds the field · CoreWeave falls"). This is non-negotiable — the myth never replaces the plain answer.
- **Defeated / victor states** — losing panel desaturates and dims; winning panel gets a quiet glow. Redundant with the verdict strip on purpose, so the outcome is never ambiguous even at a glance.
- **Second Wind button** — a real, clickable control, not a passive readout. Pressing it updates the affected stat bar and scorecard number live, and reveals a one-line strike banner explaining what happened in-fiction. Disables itself once spent.
- **Scorecard** — dimension-by-dimension tug-of-war bars beneath the fold, so the numeric truth is one scroll away from the theater above it.

---

# 3. ARCHITECTURE

## 3.1 System Overview

```text
User Challenge (via Streamlit form)
        │
        ▼
┌─────────────────────────────┐
│          War Scout           │
│  (Tavily search → research   │
│   notes per combatant)       │
└──────────────┬────────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Myth Weaver          │
│  (epithets, weapons, curses) │
└──────────────┬────────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Fight Engine          │
│  (dimension scoring under     │
│   battlefield weights,        │
│   verdict, Second Wind)       │
└──────────────┬────────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Blood Chronicler        │
│  (verdict statement + saga)   │
└──────────────┬────────────────┘
               │
               ▼
      Fight Card UI (Streamlit)
   + Hall of Fame / Graveyard entry
```

Four nodes, one straight line. No branching orchestration needed for MVP — a plain sequential pipeline (LangGraph optional, a Python function chain is enough to start).

## 3.2 Core Data Objects

- **Faction / Player**
- **ResearchNotes** — capabilities, limitations, pricing signal, source links (plain fields, no confidence-tier schema — kept simple deliberately)
- **MythicProfile** (epithet, archetype, weapons, fatal flaws, battle style)
- **Battlefield** (name + dimension weight modifiers)
- **DimensionScorecard**
- **BattleResult** (winner, loser, margin, Second Wind used y/n, decisive blows)
- **Chronicle** (verdict line + full narrative)
- **CodexEntry** (stored war for Hall of Fame / Graveyard — object defined now, persistence and browsing UI land in Phase 2)

## 3.3 Tech Stack

| Layer            | Choice                                      | Reason |
|------------------|---------------------------------------------|--------|
| Language         | Python                                      | Speed + agent ecosystem |
| Orchestration    | Plain function chain for MVP; LangGraph if it later needs branching | Don't add orchestration weight the MVP doesn't need |
| LLMs             | One strong creative model (Claude)          | Chronicle quality matters more than model-switching |
| Research         | **Tavily only**                             | Free tier (1,000 searches/mo) is enough for a portfolio demo; agent-friendly clean output; one tool means no fallback logic to build or debug |
| Schemas          | Pydantic                                    | Keep the research/myth boundary structurally enforced |
| UI               | Streamlit + CSS injection                   | Gaming-page feel without a JS framework; matches "not much complication" |
| Persistence      | SQLite / JSON Codex                         | Hall of Fame + Graveyard |

Deliberately dropped from earlier versions: multiple search providers, the six-agent council, and confidence-tiered research schemas — all complexity that didn't earn its place for a fun portfolio piece.

## 3.4 The Ritual (Pipeline)

1. User submits a challenge (two combatants + battlefield) via the Streamlit form.
2. War Scout searches Tavily, returns research notes for each combatant.
3. Myth Weaver forges mythic profiles from those notes.
4. Fight Engine scores the relevant dimensions under battlefield weights and decides the winner; if a Second Wind is available, it's flagged for the UI to offer.
5. Blood Chronicler writes the verdict line, then the full saga.
6. Result renders on the fight-card UI. If the user clicks Second Wind, the Fight Engine's pre-computed comeback beat displays and the scorecard updates.
7. Result is optionally saved to the Codex.

## 3.5 Observability

Even in maximum carnage mode, the system exposes on demand:

- The real research notes used per combatant
- Dimension scores and the battlefield weight modifiers applied
- The mapping from real weakness → fatal flaw
- Whether Second Wind was triggered and what real fact it drew on

The myth is the performance. The skeleton stays inspectable — this is the one place the project stays deliberately rigorous.

---

# 4. MVP — FIRST BLOOD

**Scope for first playable version:**

- 5 core factions fully supported (Hyperscalers, NeoClouds, Sovereign/Regional, Distributed/Edge, Private/On-Prem)
- 10–14 named major players (covering all 5 factions, including at least one On-Prem champion)
- 1v1 only (free-for-all, brackets, Hall of Fame/Graveyard, and campaigns land in Phase 2 — section 4.1)
- 5 battlefields
- Full 4-agent pipeline
- Chronicle + scorecard + verdict strip
- Second Wind mechanic, functional
- Fight-card UI (battlefield banner → VS row → verdict → scorecard)
- 4–6 pre-seeded classic matchups

**Deliberately later:**

- Image generation — skipped on purpose, not deferred. Not worth the extra token cost for a portfolio demo; the fight-card UI already carries the visual weight.

---

# 4.1 PHASE 2 — SECOND BLOOD

Scoped in, not deferred indefinitely. Builds on the MVP pipeline once First Blood is stable — same four agents, same Fidelity Law, no new infrastructure required beyond what's listed here.

**Free-for-all / tournament system**
- Extends the Fight Engine from 1v1 to N-combatant free-for-alls and simple single-elimination brackets
- Reuses the existing dimension scoring — no new scoring model needed, just resolved pairwise instead of once
- UI: bracket view feeding into the same fight-card screen per matchup

**Hall of Fame / Graveyard persistence**
- Every completed `BattleResult` + `Chronicle` writes to the SQLite/JSON Codex already specified in section 3.3
- Hall of Fame: sorted by decisive wins / most-invoked Second Winds
- Graveyard: losing combatants and their fatal blow, browsable
- No new agent — this is a persistence and browsing layer on top of the existing `CodexEntry` object

**Multi-round campaigns**
- Chains several battles across different battlefields into a running storyline for the same combatants (e.g. a best-of-3 across Cost Wasteland, AI Training Killing Fields, Sovereignty Fortress)
- Each round still resolves through the normal 4-agent pipeline; the campaign layer just tracks cumulative scars and carries the Second Wind cooldown across rounds instead of resetting it each fight
- Chronicle gains a short "campaign so far" recap line before each new round's saga

---

# 5. EXAMPLE FIGHT CARD

**MAIN EVENT**

**CoreWeave, the GPU Berserker of the NeoCloud Rebellion**  
vs  
**AWS, the First God, Lord of the Infinite Bill**

**Battlefield:** AI Training Killing Fields

**Verdict:** AWS holds the field · CoreWeave falls (62–38 on GPU power, but AWS takes it on raw gravity)

**Prophecy:**  
One was born for this war.  
One *is* the war.  
Only one leaves the cluster unburnt.

*(CoreWeave's Second Wind is available — one click reveals its strongest sourced GPU-density claim as a counter-strike beat, before the verdict stands.)*

---

# 6. PORTFOLIO POSITIONING

- **infra-arbiter** = The serious, responsible Architecture Review Board system.
- **Cloud Bloodbath** = The same mind after midnight, drunk on folklore, staging cloud empires in gladiatorial combat — built small and sharp instead of sprawling.

Together they prove range: rigorous decision systems **and** a maximally creative, technically grounded, deliberately simple war machine.

---

# 7. FINAL LAW OF THE ARENA

Make it fun.  
Make it savage.  
Respect real power differences.  
Never protect sacred cows.  
Never leave the verdict in doubt.  
Let the underdog have one real swing.  
Let the blood teach the truth.

---

*End of SPEC • Design • Architecture v2*  
*Now open the gates.*
