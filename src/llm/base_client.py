"""Base LLM client interface."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseLLMClient(ABC):
    """Base class for LLM clients."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate text using the LLM.

        Args:
            system_prompt: System/instruction prompt
            user_prompt: User message
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        pass
