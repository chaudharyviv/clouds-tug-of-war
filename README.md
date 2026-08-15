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

## ⚙️ The War Council (Agent Architecture)

The system relies on a sequence of 4 specialized agents:

1. **War Scout** — Runs the search tool (Tavily), produces plain research notes (capabilities, limitations, pricing) per combatant. 
2. **Myth Weaver** — Turns technical research notes into legendary weapons, curses, epithets, and battle styles without inventing non-existent capabilities (Fidelity Law).
3. **Fight Engine** — Scores 10 cloud architectural dimensions under specific battlefield weights, decides the winner, and resolves the **Second Wind** comeback.
4. **Blood Chronicler** — Writes the full blood-soaked saga and plainly states the verdict.

---

## 🛠️ Tech Stack
- **Language**: Python
- **LLM Engine**: OpenAI (GPT-4o)
- **Research Engine**: Tavily Search API
- **UI & Visualization**: Streamlit (with gaming-inspired custom CSS injections)
- **Data Schemas**: Pydantic v2 (Enforcing the Fidelity Law between agents)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [Tavily API Key](https://tavily.com/)
- [OpenAI API Key](https://platform.openai.com/)

### 2. Setup
Clone the repository and prepare your environment:

```bash
git clone https://github.com/chaudharyviv/clouds-tug-of-war.git
cd clouds-tug-of-war

# Copy the environment file and add your keys
cp .env.example .env
```
_Edit the `.env` file and insert your `OPENAI_API_KEY` and `TAVILY_API_KEY`._

### 3. Run the Arena

On Windows, you can use the provided quick-launch script:
```powershell
.\run.ps1
```

Or run manually:
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 4. Stage the Slaughter
Open your browser to the local Streamlit URL, select your champions and the battlefield, and let the War Council decide their fate.

---

## 📜 The Fidelity Law
The Myth Weaver may be extreme. The Blood Chronicler may be unhinged.
Neither may invent capabilities that do not exist or erase well-known limitations. The War Scout's research notes remain the source of truth. The underlying technical logic (Dimension Scorecard) is always inspectable.
