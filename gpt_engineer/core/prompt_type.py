from typing import Dict, Optional

class PromptType:
    def __init__(self, system_prompt: str, user_prompt: str):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def get_user_prompt(self) -> str:
        return self.user_prompt

    def process_response(self, response: str, files_dict: Dict[str, str]) -> Dict[str, str]:
        """
        Process the LLM response to create or edit files.
        This method should be overridden by subclasses for specific behavior.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class CodeGenerationPrompt(PromptType):
    def __init__(self, user_prompt: str):
        system_prompt = "Generate code based on the following requirements."
        super().__init__(system_prompt, user_prompt)

    def process_response(self, response: str, files_dict: Dict[str, str]) -> Dict[str, str]:
        # Implement logic to create or edit files based on the response
        return files_dict
