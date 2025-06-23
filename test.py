import unittest
from ai_prompt_generator import (
    AIImagePromptGenerator,
    PromptElements,
)  # Import the class and dataclass


class TestPromptGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = AIImagePromptGenerator(
            api_key="test_key"
        )  # Replace with a valid API key or mock

    def test_generate_prompt_basic(self):
        elements = PromptElements(subject="cat", style="photorealistic")
        prompt = self.generator.create_basic_prompt(elements)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_generate_prompt_empty_input(self):
        elements = PromptElements(subject="", style="")
        prompt = self.generator.create_basic_prompt(elements)
        self.assertIsInstance(prompt, str)

    def test_generate_prompt_with_details(self):
        elements = PromptElements(
            subject="dog", style="cartoon", details="wearing a hat"
        )
        prompt = self.generator.create_basic_prompt(elements)
        self.assertIn("hat", prompt)


if __name__ == "__main__":
    unittest.main()
