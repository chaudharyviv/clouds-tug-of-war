from src.services.llm import LLMService

class BaseAgent:
    def __init__(self, name: str, role: str, personality: str, temperature: float = 0.2):
        self.name = name
        self.role = role
        self.personality = personality
        # Controls creative variance per agent: cold/analytical roles (Scout, Fight
        # Engine) stay low for reliable facts and parseable JSON; theatrical roles
        # (Myth Weaver, Blood Chronicler) run hot for maximum flourish.
        self.temperature = temperature

    def get_system_prompt(self) -> str:
        return (
            f"You are the {self.name}, the {self.role} of the War Council.\n"
            f"Your personality is: {self.personality}.\n\n"
            f"Keep your response strictly aligned with your role, tone, and goals."
        )

    def query_llm(self, prompt: str) -> str:
        return LLMService.query(prompt, system_prompt=self.get_system_prompt(), temperature=self.temperature)

    def query_llm_structured(self, prompt: str, response_model):
        return LLMService.query_structured(
            prompt, response_model, system_prompt=self.get_system_prompt(), temperature=self.temperature
        )
