import json
import os
from typing import List
from src.models.battle import CodexEntry

CODEX_FILE_PATH = "codex_history.json"

class CodexService:
    @staticmethod
    def save_entry(entry: CodexEntry) -> None:
        """
        Saves a fight record (CodexEntry) into the persistent JSON history.
        """
        entries = CodexService.load_entries()
        entries.append(entry)
        
        # Write to JSON file
        try:
            with open(CODEX_FILE_PATH, "w") as f:
                # Convert list of entries to serialized JSON array
                serialized = [json.loads(e.model_dump_json()) for e in entries]
                json.dump(serialized, f, indent=4)
        except Exception as e:
            print(f"Error saving to Codex: {e}")

    @staticmethod
    def load_entries() -> List[CodexEntry]:
        """
        Loads all fight records from the JSON history.
        """
        if not os.path.exists(CODEX_FILE_PATH):
            return []
            
        try:
            with open(CODEX_FILE_PATH, "r") as f:
                data = json.load(f)
                return [CodexEntry.model_validate(item) for item in data]
        except Exception as e:
            print(f"Error loading Codex entries: {e}")
            return []
            
    @staticmethod
    def clear_codex() -> None:
        """
        Clears the persistent Codex history.
        """
        if os.path.exists(CODEX_FILE_PATH):
            try:
                os.remove(CODEX_FILE_PATH)
            except Exception as e:
                print(f"Error clearing Codex: {e}")
