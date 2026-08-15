from src.agents.base import BaseAgent
from src.models.combatant import MythicProfile
from src.models.battle import ResearchNotes

class MythWeaver(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Myth Weaver",
            role="Myth-maker and forge of weapons and curses",
            personality="Unhinged myth-maker, dramatic, metal-inspired, poetic. You view the cloud as a chaotic realm of gods, warlords, and spells."
        )

    def forge_profile(self, name: str, notes: ResearchNotes) -> MythicProfile:
        """
        Converts real ResearchNotes into a MythicProfile (epithets, weapons, curses/fatal flaws) 
        while strictly adhering to the Fidelity Law (all myth is based on real facts).
        """
        prompt = (
            f"You must forge a Mythic Profile for the combatant: {name}\n"
            f"Ground your mythic items strictly on these real-world research notes:\n"
            f"Capabilities: {notes.capabilities}\n"
            f"Limitations: {notes.limitations}\n"
            f"Pricing Signal: {notes.pricing_signal}\n\n"
            f"Fidelity Law constraints:\n"
            f"- Each legendary weapon MUST directly map to a specific capability.\n"
            f"- Each curse/fatal flaw MUST directly map to a real limitation or pricing drawback.\n"
            f"- Do not invent powers or remove weaknesses.\n"
            f"- Create a dramatic epithet (e.g. Master of Gravitational Lock-in) and describe their battle style."
        )
        
        return self.query_llm_structured(prompt, MythicProfile)
