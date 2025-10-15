"""OpenAI client for GPT models."""

from typing import Optional
from loguru import logger

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not installed. Install with: pip install openai")

from .base_client import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    """Client for OpenAI GPT models."""

    def __init__(
        self,
        api_key: str,
        model_id: str = "gpt-4",
        **kwargs
    ):
        """
        Initialize OpenAI client.

        Args:
            api_key: OpenAI API key
            model_id: Model to use (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")

        self.model_id = model_id
        self.client = OpenAI(api_key=api_key)
        logger.info(f"Initialized OpenAIClient with model: {model_id}")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate text using OpenAI.

        Args:
            system_prompt: System instructions
            user_prompt: User message
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
