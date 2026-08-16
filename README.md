# ⚔️ CLOUD BLOODBATH ⚔️

**Tone: Folklore × Thug-of-War × Absolute Cloud Carnage**  
**Domain: Multi-Faction War for the Cloud Realms**

> This is not a cloud comparison tool.  
> This is not a Gartner quadrant.  
> This is a mythic bloodsport where cloud empires, warbands, and guerrilla tribes fight for dominion over compute, data, and the future.

**Cloud Bloodbath** is a small, high-creativity multi-agent system that stages savage, theatrical, and technically grounded wars between cloud factions and named players. 

Users throw empires and upstarts into the arena. The system researches their real power, turns strengths into legendary weapons and weaknesses into curses, runs a dimension tug-of-war under battlefield rules, and writes a blood-soaked chronicle that declares who survives - clearly, not ambiguously.

---

## 🌩️ Core Fantasy & Factions

The cloud is not a market. It is a collection of warring realms:

- **Hyperscalers (AWS, Azure, GCP)** — The three ancient God-Empires. Infinite scale, deep magic, gravitational lock-in, and crushing tribute.
- **NeoClouds (CoreWeave, Lambda)** — The new AI warbands. Lean, specialized, hungry, born for GPU bloodsport.
- **Sovereign / Regional Clouds (OVHcloud)** — Border kingdoms obsessed with data walls and national shields.
- **Distributed / Edge Tribes (Cloudflare, Vercel)** — Guerrilla fighters living at the fringes. Fast locally, fragile in open war.
- **Private / On-Prem Empires** — The old fortress kingdoms still trying to hold their walls.

---

## 🏗️ Project Structure

```
clouds-tug-of-war/
├── app.py                      # Streamlit entry point
├── src/
│   ├── agents/                 # Multi-agent pipeline
│   │   ├── base.py             # BaseAgent with LLM integration
│   │   ├── scout.py            # WarScout - research agent
│   │   ├── weaver.py           # MythWeaver - narrative transformer
│   │   ├── engine.py           # FightEngine - scoring & combat resolver
│   │   ├── chronicler.py       # BloodChronicler - saga writer
│   │   └── __init__.py
│   ├── models/                 # Pydantic data models
│   │   ├── battle.py           # ResearchNotes, BattleResult, Chronicle, CodexEntry
│   │   ├── battlefield.py      # Battlefield, COMEBACK_MULTIPLIER
│   │   ├── combatant.py        # FactionType, MythicProfile, Champion
│   │   └── __init__.py
│   ├── services/               # Core services
│   │   ├── llm.py              # LLMService for OpenAI/GPT-4o
│   │   ├── search.py           # Tavily search integration
│   │   ├── orchestrator.py     # ArenaOrchestrator - 4-agent pipeline
│   │   ├── codex.py            # Persistent battle history
│   │   └── __init__.py
│   ├── ui/                     # Streamlit views & components
│   │   ├── views.py            # ArenaViews - main view routing
│   │   ├── components.py       # Reusable UI components
│   │   └── __init__.py
│   └── static/
│       └── style.css           # Gaming-inspired custom CSS
├── design/
│   └── v3_fight_engine_design.md
├── .env                        # API keys (not committed)
├── .env.example                # Environment template
└── requirements.txt            # Python dependencies
```

---

## ⚙️ The War Council (Agent Architecture)

The system relies on a sequence of 4 specialized agents, each inheriting from `BaseAgent`:

### BaseAgent (`src/agents/base.py`)
- Common base class for all agents
- Manages name, role, personality, and temperature settings
- Provides `query_llm()` and `query_llm_structured()` methods
- Temperature tuning: analytical roles (Scout, Engine) = 0.15-0.2; theatrical roles (Weaver, Chronicler) = 0.95

### 1. War Scout (`src/agents/scout.py`)
- **Temperature**: 0.2 (cold, factual)
- Uses Tavily Search API to research combatants
- Produces `ResearchNotes` with:
  - `capabilities`: Real-world strengths and technical assets
  - `limitations`: Real-world gaps and bottlenecks
  - `pricing_signal`: Unit economics and pricing model
  - `source_links`: Attribution URLs

### 2. Myth Weaver (`src/agents/weaver.py`)
- **Temperature**: 0.95 (hot, theatrical)
- Transforms technical research into mythic profiles
- Generates:
  - `epithet`: Heroic moniker (e.g., "The Gravitational Titan")
  - `weapons`: Legendary capabilities derived from real strengths
  - `fatal_flaws`: Curses derived from real limitations
  - `battle_style`: Combat approach fitting the faction type

### 3. Fight Engine (`src/agents/engine.py`)
- **Temperature**: 0.15 (hyper-logical, objective)
- Scores combatants across 10 architectural dimensions:
  - Compute & Infrastructure, Storage & Databases, Networking, Security, Pricing, etc.
- Applies battlefield-specific weights to dimensions
- Calculates **Tactical Advantage** bonus (+15 max) based on battlefield rules
- Determines winner via weighted aggregate scoring
- Manages **Second Wind** comeback mechanics

### 4. Blood Chronicler (`src/agents/chronicler.py`)
- **Temperature**: 0.95 (drunk bard + metal commentator)
- Writes theatrical saga incorporating weapons and fatal flaws
- Produces plain-text `verdict` strip for unambiguous results
- Returns `Chronicle` with:
  - `verdict`: "WINNER_NAME holds the field · LOSER_NAME falls (reason)"
  - `saga`: Full bardic narrative of the combat

---

## 📊 Data Models (`src/models/`)

### ResearchNotes
```python
capabilities: List[str]          # Real strengths
limitations: List[str]           # Real gaps
pricing_signal: str              # Unit economics
source_links: List[str]          # Attribution
```

### Champion
```python
name: str                        # Combatant name
faction_type: FactionType        # Hyperscaler, NeoCloud, etc.
mythic_profile: MythicProfile    # Epithet, weapons, curses
```

### MythicProfile
```python
epithet: str                     # Heroic moniker
weapons: List[str]               # Legendary capabilities
fatal_flaws: List[str]           # Curses
battle_style: str                # Combat approach
```

### Battlefield
```python
name: str                        # Battlefield name
description: str                 # Flavor text
rewards: str                     # What this terrain favors
suffers: str                     # What it punishes
tactical_rule: str               # Specific rule (e.g., "GPU density")
comeback_profile: str            # "high", "medium", "low"
dimensions: Dict[str, float]     # Dimension weights (0.5-2.0)
```

### BattleResult
```python
winner_name: str
loser_name: str
margin: float                    # Score differential
score_a: float                   # Combatant A total
score_b: float                   # Combatant B total
second_wind_triggered: bool
second_wind_fact: str            # Capability used for comeback
second_wind_impact: float        # Score swing
decisive_blows: List[str]        # Key technical reasons
scorecards: Dict[str, DimensionScorecard]
tactical_capability_a/b: str     # Relevant capability
tactical_bonus_a/b: float        # Bonus points
```

---

## 🔄 Orchestration Pipeline (`src/services/orchestrator.py`)

The `ArenaOrchestrator` class manages the full 4-agent sequence:

```
┌─────────────────────────────────────────────────────────────┐
│                    perform_ritual()                         │
├─────────────────────────────────────────────────────────────┤
│ 1. WarScout.analyze_combatant()                            │
│    → ResearchNotes for Champion A & B                      │
│                                                             │
│ 2. MythWeaver.forge_profile()                              │
│    → MythicProfile for Champion A & B                      │
│                                                             │
│ 3. FightEngine.score_battle()                              │
│    → BattleResult with weighted scores, winner, margin     │
│    → Second Wind fact + reason + impact                    │
│                                                             │
│ 4. BloodChronicler.write_chronicle()                       │
│    → Chronicle with verdict + saga                         │
└─────────────────────────────────────────────────────────────┘
```

Second Wind activation recalculates scores and rewrites the chronicle with comeback context.

---

## 🎮 UI Layer (`src/ui/`)

### views.py (ArenaViews)
- `render_setup_view()` — Champion and battlefield selection
- `render_fight_view()` — Live battle progress and results
- `render_codex_view()` — Historical battle archive

### components.py
- Reusable Streamlit components for the arena interface

Custom CSS (`src/static/style.css`) provides the gaming/fantasy aesthetic with ember glows and metallic textures.

---

## ⚡ The Second Wind

Every duel gives the losing side exactly **one** comeback beat.

1. Fight Engine picks the loser's single strongest capability *relevant to that battlefield* (not just flashiest stat overall)
2. User clicks "Second Wind" button in UI
3. Score recalculates: `(relevance / 100) × 20 × comeback_multiplier × underdog_factor`
4. Scorecard and margin update live
5. Strike banner explains what happened in-fiction

---

## 🎯 The Verdict

The saga can get as unhinged as the Chronicler wants — the verdict strip never does. It's:
- Loud, permanent, pinned to top of results page
- Plain language, 3-second legibility
- Format: "WINNER_NAME holds the field · LOSER_NAME falls (reason)"

---

## 📜 The Fidelity Law

The Myth Weaver may be extreme. The Blood Chronicler may be unhinged.  
Neither may invent capabilities that do not exist or erase well-known limitations.  
The War Scout's research notes remain the source of truth.  
The underlying technical logic (Dimension Scorecard) is always inspectable.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| LLM Engine | OpenAI (GPT-4o) via `src/services/llm.py` |
| Research | Tavily Search API via `src/services/search.py` |
| Data Schemas | Pydantic v2 |
| UI | Streamlit + custom CSS |
| Persistence | Codex history via `src/services/codex.py` |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [Tavily API Key](https://tavily.com/)
- [OpenAI API Key](https://platform.openai.com/)

### 2. Setup
```bash
git clone https://github.com/chaudharyviv/clouds-tug-of-war.git
cd clouds-tug-of-war

# Copy the environment file and add your keys
cp .env.example .env
```
Edit `.env` and insert your `OPENAI_API_KEY` and `TAVILY_API_KEY`.

### 3. Run the Arena

**Windows (PowerShell):**
```powershell
.\run.ps1
```

**Manual:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 4. Stage the Slaughter
Open the local Streamlit URL, select champions and battlefield, let the War Council decide their fate.

---

## 🔧 Configuration

Environment variables in `.env`:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key |
| `TAVILY_API_KEY` | Tavily Search API key |
| `PRIMARY_MODEL` | Optional: override default model (e.g., `anthropic/claude-3-5-sonnet`) |
| `CODEX_PATH` | Optional: path to battle history database |