import json
from typing import Dict, Optional

from gpt_engineer.core.prompt_type import PromptType


class Prompt:
    def __init__(
        self,
        prompt_type: PromptType,
        image_urls: Optional[Dict[str, str]] = None,
        entrypoint_prompt: str = "",
    ):
        self.prompt_type = prompt_type
        self.image_urls = image_urls
        self.entrypoint_prompt = entrypoint_prompt

    def __repr__(self):
        return f"Prompt(prompt_type={self.prompt_type!r}, image_urls={self.image_urls!r})"

    def to_langchain_content(self):
        content = [{"type": "text", "text": f"Request: {self.prompt_type.get_user_prompt()}"}]

        if self.image_urls:
            for name, url in self.image_urls.items():
                image_content = {
                    "type": "image_url",
                    "image_url": {
                        "url": url,
                        "detail": "low",
                    },
                }
                content.append(image_content)

        return content

    def to_dict(self):
        return {
            "system_prompt": self.prompt_type.get_system_prompt(),
            "user_prompt": self.prompt_type.get_user_prompt(),
            "image_urls": self.image_urls,
            "entrypoint_prompt": self.entrypoint_prompt,
        }

    def to_json(self):
        return json.dumps(self.to_dict())
