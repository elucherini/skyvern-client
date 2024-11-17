from pathlib import Path
from typing import Any
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, ConfigDict

"""
Collection of utils from the Skyvern codebase taken under license AGPL v3.0.
"""


PARENT_DIR = Path(__file__).parent.parent


class PromptEngine:
    def __init__(self, prompts_dir: Path = PARENT_DIR / "skyvern-prompts") -> None:
        """
        Initialize the PromptEngine.
        """

        self.env = Environment(loader=FileSystemLoader(prompts_dir))

    def load_prompt(self, template: str, **kwargs: Any) -> str:
        """
        Load and populate the specified template.

        Args:
            template (str): The name of the template to load.
            **kwargs: The arguments to populate the template with.

        Returns:
            str: The populated template.
        """
        try:
            jinja_template = self.env.get_template(f"{template}.j2")
            return jinja_template.render(**kwargs)
        except Exception:
            print("Failed to load prompt.", template, kwargs.keys())
            raise
