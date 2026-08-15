from src.agents.base import BaseAgent
from src.models.battle import ResearchNotes
from src.services.search import SearchService
import json

class WarScout(BaseAgent):
    def __init__(self):
        super().__init__(
            name="War Scout",
            role="Scout of capabilities and limitations",
            personality="Cold, precise, highly analytical. You present technical facts and strip away marketing fluff.",
            temperature=0.2
        )

    def analyze_combatant(self, combatant_name: str) -> ResearchNotes:
        """
        Runs web searches for the combatant and extracts capabilities, limitations, and pricing signals.
        """
        # Execute multiple search queries to gather comprehensive data
        queries = [
            f"{combatant_name} cloud technical capabilities architecture",
            f"{combatant_name} cloud scale limitations outages pricing issues"
        ]
        
        search_results = []
        source_links = []
        for query in queries:
            results = SearchService.search(query, max_results=3)
            for res in results:
                search_results.append(f"Source: {res['title']} ({res['url']})\nContent: {res['content']}\n")
                source_links.append(res['url'])
                
        compiled_data = "\n".join(search_results)
        
        prompt = (
            f"Extract capabilities, limitations, and pricing signals for the combatant: {combatant_name}\n"
            f"Use the following search results to ground your findings:\n\n"
            f"{compiled_data}\n\n"
            f"Formulate a precise research profile for the combatant. Do not invent any facts."
        )
        
        # Query structured output matching ResearchNotes Pydantic schema
        notes = self.query_llm_structured(prompt, ResearchNotes)
        # Ensure raw source links are appended
        notes.source_links = list(set(notes.source_links + source_links))
        
        return notes
