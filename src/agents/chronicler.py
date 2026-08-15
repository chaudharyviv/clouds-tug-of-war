from src.agents.base import BaseAgent
from src.models.battle import BattleResult, Chronicle
from src.models.combatant import Champion
from src.models.battlefield import Battlefield

class BloodChronicler(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Blood Chronicler",
            role="Scribe of the battlefield saga",
            personality="Drunk bard mixed with a metal commentator. Passionate, bloodthirsty, theatrical, and loud. You tell tales of absolute cloud carnage.",
            temperature=0.95
        )

    def write_chronicle(
        self, 
        champion_a: Champion, 
        champion_b: Champion, 
        battlefield: Battlefield, 
        result: BattleResult
    ) -> Chronicle:
        """
        Drafts a theatrical battle saga along with a plain-text, unambiguous verdict strip.
        """
        prompt = (
            f"Write the chronicle for this duel on the battlefield '{battlefield.name}' ({battlefield.description}).\n\n"
            f"Fighter A: {champion_a.name} ({champion_a.mythic_profile.epithet if champion_a.mythic_profile else 'The Challenger'})\n"
            f"Weapons: {champion_a.mythic_profile.weapons if champion_a.mythic_profile else []}\n"
            f"Curses: {champion_a.mythic_profile.fatal_flaws if champion_a.mythic_profile else []}\n\n"
            f"Fighter B: {champion_b.name} ({champion_b.mythic_profile.epithet if champion_b.mythic_profile else 'The Challenger'})\n"
            f"Weapons: {champion_b.mythic_profile.weapons if champion_b.mythic_profile else []}\n"
            f"Curses: {champion_b.mythic_profile.fatal_flaws if champion_b.mythic_profile else []}\n\n"
            f"Verdict Stats:\n"
            f"- Winner: {result.winner_name}\n"
            f"- Loser: {result.loser_name}\n"
            f"- Decisive Blows: {result.decisive_blows}\n"
            f"- Second Wind Used: {result.second_wind_triggered}\n\n"
            f"Formatting Rules:\n"
            f"1. You MUST generate a clear 'verdict' string in the exact format: 'WINNER_NAME holds the field · LOSER_NAME falls (brief reason)'\n"
            f"2. Write a 'saga' (narrative text) describing the combat in a theatrical, epic tone. Incorporate their weapons and fatal flaws explicitly into the action. Describe how the battlefield's rules swung the fight. Keep the outcome completely clear."
        )
        
        return self.query_llm_structured(prompt, Chronicle)
