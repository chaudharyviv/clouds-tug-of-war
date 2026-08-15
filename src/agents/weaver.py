from src.agents.base import BaseAgent
from src.models.combatant import MythicProfile
from src.models.battle import ResearchNotes

class MythWeaver(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Myth Weaver",
            role="Myth-maker and forge of weapons and curses",
            personality="Unhinged myth-maker, dramatic, metal-inspired, poetic. You view the cloud as a chaotic realm of gods, warlords, and spells.",
            temperature=0.8
        )

    def forge_profile(self, name: str, notes: ResearchNotes) -> MythicProfile:
        """
        Converts real ResearchNotes into a MythicProfile (epithets, weapons, curses/fatal flaws)
        while strictly adhering to the Fidelity Law (all myth is based on real facts).
        """
        caps_formatted = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(notes.capabilities)) or "  (none listed)"
        limits_formatted = "\n".join(f"  {i+1}. {l}" for i, l in enumerate(notes.limitations)) or "  (none listed)"
        prompt = (
            f"You must forge a Mythic Profile for the combatant: {name}\n"
            f"Ground your mythic items strictly on these real-world research notes:\n"
            f"Capabilities:\n{caps_formatted}\n"
            f"Limitations:\n{limits_formatted}\n"
            f"Pricing Signal: {notes.pricing_signal}\n\n"
            f"Fidelity Law constraints (non-negotiable — the theatrics can be extreme, the grounding cannot slip):\n"
            f"- Produce exactly one weapon per capability listed above, in the same order, each one a direct "
            f"dramatization of that specific capability — not a generic power.\n"
            f"- Produce exactly one curse/fatal flaw per limitation listed above (plus the pricing signal if it "
            f"reads as a drawback), in the same order, each a direct dramatization of that specific weakness.\n"
            f"- Do not invent powers or weaknesses that aren't traceable to one of the lines above.\n"
            f"- Do not soften or omit a listed limitation just because it's inconvenient for the myth.\n"
            f"- Create a dramatic epithet (e.g. Master of Gravitational Lock-in) and describe their battle style."
        )

        profile = self.query_llm_structured(prompt, MythicProfile)

        # Light fidelity check: flag (don't block) if the weapon/curse counts drift from the
        # research notes — the most common symptom of the model wandering off-source at high
        # temperature. Surfaced in server logs for now; promote to a UI warning if it recurs.
        if notes.capabilities and len(profile.weapons) != len(notes.capabilities):
            print(
                f"WARNING: Fidelity drift for {name} — {len(profile.weapons)} weapons forged "
                f"from {len(notes.capabilities)} capabilities."
            )
        if notes.limitations and len(profile.fatal_flaws) < len(notes.limitations):
            print(
                f"WARNING: Fidelity drift for {name} — only {len(profile.fatal_flaws)} curses forged "
                f"from {len(notes.limitations)} limitations."
            )

        return profile
