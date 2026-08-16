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
├── app.py                      # Streamlit entry point & app bootstrapping
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
│   │   ├── codex.py            # Persistent battle history (JSON)
│   │   └── __init__.py
│   ├── ui/                     # Streamlit views & components
│   │   ├── views.py            # ArenaViews - view routing & business logic
│   │   ├── components.py       # Reusable render functions
│   │   └── __init__.py
│   └── static/
│       └── style.css           # Neural War Neon cyberpunk theme
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
- Scores combatants across 10 architectural dimensions
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

## 🎮 UI Layer

### app.py (Entry Point)

The main Streamlit application handles:

**Page Configuration**
```python
st.set_page_config(
    page_title="Cloud Bloodbath - Multi-Agent Tug-of-War",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Password Protection (`APP_PASSWORD`)**
- Optional gate behind a single shared password
- Set `APP_PASSWORD` in `.env` to enable
- Uses `hmac.compare_digest()` for secure comparison
- Without `APP_PASSWORD`, gates stay open for local development

**Session States**
- `battle_state`: "setup" → "fighting"
- `app_tab`: "Arena" ↔ "Codex History"
- `ritual_executed`: Tracks if battle has been computed
- Caches `champion_a`, `champion_b`, `battlefield`, `notes_a`, `notes_b`, `battle_result`, `battle_chronicle`

**Sidebar**
- Navigation radio: "Arena" | "Codex History"
- Displays: Oracle model, Tavily API status, Fidelity Law status

---

### views.py (ArenaViews)

Main view controller with three rendering methods:

#### `render_setup_view()`
- **Fighter Selection Mode** (segmented control):
  - "Ancient Grudge" — Preset rivalries (GPU Rebellion, Edge Skirmish, Sovereignty Clash, Cost Bleedout)
  - "Choose Your Champions" — Custom selection from `DEFAULT_CHAMPIONS` or forge new
- **Champion columns** — Left (ember color) vs Right (cyan color)
- **Custom challenger forge** — Name, faction, description
- **Battlefield selection** — Dropdown with terrain rules display
- **"Stage the slaughter"** button triggers the ritual

#### `render_fight_view()`
1. `render_battlefield_banner()` — Terrain header with rewards/suffers
2. `render_vs_row()` — Fighter cards with diagonal cuts, victor/defeated states
3. `render_weapons_and_flaws()` — Weapon list (cyan) & curses (blood)
4. `render_prophecy()` — Flavor text
5. `render_verdict_strip()` — **Sticky** plain-language verdict
6. `render_score_totals()` — Power balance numbers
7. **Second Wind** — Button for loser comeback, recalculates scores
8. `render_scorecard()` — Dimension tug-of-war bars
9. `render_tactical_advantage()` — Battlefield-relevant capabilities
10. `render_decisive_blows()` — Key technical reasons
11. `render saga_box()` — Full bardic chronicle
12. **Fidelity Law expander** — Inspectable raw research notes
13. **Save to Codex** button — Persists battle to JSON
14. **Stage another fight** — Reset flow

#### `render_codex_view()`
- **Hall of Fame** — Win leaderboard with per-battlefield breakdown
- **Graveyard** — List of fallen champions
- **Archive Halls** — Expandable cards with full battle details
- **"Burn the archives"** — Clear all history

---

### components.py (Render Functions)

Helper functions for UI rendering:

| Function | Purpose |
|----------|---------|
| `render_battlefield_banner()` | Terrain header with pulsing name glow |
| `render_vs_row()` | Fighter cards with diagonal clip-path, VS mark, dynamic victor/defeated styling |
| `render_weapons_and_flaws()` | Side-by-side weapon (cyan) and curse (blood) lists |
| `render_prophecy()` | Flavor prophecy line above verdict |
| `render_verdict_strip()` | Sticky, high-contrast verdict bar |
| `render_score_totals()` | Power balance scores under verdict |
| `render_scorecard()` | 10-dimension tug-of-war with weighted scores |
| `render_tactical_advantage()` | Battlefield-relevant capabilities with bonuses |
| `render_decisive_blows()` | Battle log styled decisive factors |

**Internal helpers:**
- `_render_html()` — Flattens HTML fragments to prevent Streamlit code-block parsing
- `_stat_rows()` — Extracts dimension scores for fighter stat blocks

---

### style.css (Neural War Neon Theme)

Cyberpunk color palette:
- `--bg-void`: #050318 (near-black void)
- `--ember`: #b026ff (electric violet)
- `--blood`: #ff2d95 (neon magenta)
- `--cyan`: #00eaff (electric cyan)
- `--bone`: #eef0ff (near-white)

**Key animations:**
- `battle-glow-pulse` — Victor glow effect
- `victor-crown-glow` — Winner text shimmer
- `battlefield-name-pulse` — Battlefield name pulse
- `screen-shake-impact` — VS row impact shake
- `second-wind-pulse` — Comeback banner animation

**Visual elements:**
- Diagonal fighter card edges with clip-path
- Gradient divider lines between sections
- Sticky verdict strip (top: 3.5rem)
- Weapon lists (cyan) vs Curses (blood)
- Tug-of-war dimension bars with dynamic fill

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
- **Sticky** — Survives scrolling, pinned at top
- **Loud** — Pinned verdict strip with ember border glow
- **Plain** — 3-second legibility: "WINNER_NAME holds the field · LOSER_NAME falls (reason)"

---

## 📜 The Fidelity Law

The Myth Weaver may be extreme. The Blood Chronicler may be unhinged.  
Neither may invent capabilities that do not exist or erase well-known limitations.  
The War Scout's research notes remain the source of truth.  
The underlying technical logic (Dimension Scorecard) is always inspectable via the "Peer behind the myth" expander.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| LLM Engine | OpenAI (GPT-4o / GPT-4o-mini) via `src/services/llm.py` |
| Research | Tavily Search API via `src/services/search.py` |
| Data Schemas | Pydantic v2 |
| UI Framework | Streamlit + custom CSS |
| Theme | Neural War Neon (CSS variables, animations) |
| Persistence | JSON file via `src/services/codex.py` |
| Auth | Optional password gate via `APP_PASSWORD` env var |

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

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | — |
| `TAVILY_API_KEY` | Tavily Search API key | — |
| `PRIMARY_MODEL` | Override LLM model | `openai/gpt-4o` |
| `CODEX_PATH` | Battle history file | `codex_history.json` |
| `APP_PASSWORD` | Optional password gate | (none — open) |