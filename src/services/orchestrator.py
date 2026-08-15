from src.models.combatant import Champion
from src.models.battlefield import Battlefield
from src.models.battle import ResearchNotes, BattleResult, Chronicle, CodexEntry
from src.agents.scout import WarScout
from src.agents.weaver import MythWeaver
from src.agents.engine import FightEngine
from src.agents.chronicler import BloodChronicler
from typing import Tuple
import uuid
from datetime import datetime

class ArenaOrchestrator:
    def __init__(self):
        self.scout = WarScout()
        self.weaver = MythWeaver()
        self.engine = FightEngine()
        self.chronicler = BloodChronicler()

    def perform_ritual(
        self, 
        champion_a: Champion, 
        champion_b: Champion, 
        battlefield: Battlefield
    ) -> Tuple[Champion, Champion, ResearchNotes, ResearchNotes, BattleResult, Chronicle]:
        """
        Runs the full 4-agent pipeline sequentially to resolve the duel.
        """
        # Step 1: War Scout gathers technical facts
        notes_a = self.scout.analyze_combatant(champion_a.name)
        notes_b = self.scout.analyze_combatant(champion_b.name)
        
        # Step 2: Myth Weaver forges epithets, weapons, and curses
        champion_a.mythic_profile = self.weaver.forge_profile(champion_a.name, notes_a)
        champion_b.mythic_profile = self.weaver.forge_profile(champion_b.name, notes_b)
        
        # Step 3: Fight Engine scores the dimensions and decides winner
        result = self.engine.score_battle(champion_a, notes_a, champion_b, notes_b, battlefield)
        
        # Step 4: Blood Chronicler writes the epic tale
        chronicle = self.chronicler.write_chronicle(champion_a, champion_b, battlefield, result)
        
        return champion_a, champion_b, notes_a, notes_b, result, chronicle

    def apply_second_wind(
        self, 
        champion_a: Champion, 
        champion_b: Champion, 
        battlefield: Battlefield,
        result: BattleResult
    ) -> Tuple[BattleResult, Chronicle]:
        """
        Recalculates scores and drafts a revised chronicle based on Second Wind activation.
        """
        if result.second_wind_triggered:
            # Cannot trigger twice
            return result, self.chronicler.write_chronicle(champion_a, champion_b, battlefield, result)
            
        # Mark as triggered
        result.second_wind_triggered = True
        
        # Adjust score margins based on the impact
        # We subtract the impact from the winner's score or add it to the loser's score
        original_margin = result.margin
        result.margin = max(0.0, round(original_margin - result.second_wind_impact, 2))
        
        # If the margin hits 0 and gets flipped, check if winner changes (Fidelity Law allows rare upsets)
        if result.margin == 0.0 and result.second_wind_impact > original_margin:
            # Swap winner and loser names
            old_winner = result.winner_name
            result.winner_name = result.loser_name
            result.loser_name = old_winner
            result.margin = round(result.second_wind_impact - original_margin, 2)
            
        # Re-write the chronicle reflecting the comeback
        new_chronicle = self.chronicler.write_chronicle(champion_a, champion_b, battlefield, result)
        return result, new_chronicle
