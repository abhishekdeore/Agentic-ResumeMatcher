"""AWS Bedrock client for Claude models."""

import json
import boto3
from typing import Optional
from loguru import logger

from .base_client import BaseLLMClient


class BedrockClient(BaseLLMClient):
    """Client for AWS Bedrock Claude models."""

    def __init__(
        self,
        model_id: str = "us.anthropic.claude-sonnet-4-20250514-v1:0",
        region: str = "us-west-2",
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None
    ):
        """
        Initialize Bedrock client.

        Args:
            model_id: Bedrock model ID to use
            region: AWS region
            aws_access_key_id: AWS access key (optional, uses env if not provided)
            aws_secret_access_key: AWS secret key (optional, uses env if not provided)
        """
        self.model_id = model_id
        self.region = region

        # Create boto3 client
        session_kwargs = {"region_name": region}
        if aws_access_key_id and aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = aws_access_key_id
            session_kwargs["aws_secret_access_key"] = aws_secret_access_key

        self.client = boto3.client("bedrock-runtime", **session_kwargs)
        logger.info(f"Initialized BedrockClient with model: {model_id}")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """
        Generate text using Claude via Bedrock Converse API.

        Args:
            system_prompt: System instructions
            user_prompt: User message
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Generated text
        """
        try:
            # Use Converse API (newer, simpler method)
            response = self.client.converse(
                modelId=self.model_id,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": user_prompt}]
                    }
                ],
                system=[{"text": system_prompt}],
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                    "topP": 0.9
                }
            )

            # Extract text from response
            output_message = response.get("output", {}).get("message", {})
            content_blocks = output_message.get("content", [])

            if content_blocks and len(content_blocks) > 0:
                text = content_blocks[0].get("text", "")
                return text
            else:
                raise ValueError("No content in response")

        except Exception as e:
            logger.error(f"Bedrock API error: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")


class MockLLMClient(BaseLLMClient):
    """Mock LLM client for testing without API calls."""

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> str:
        """Return mock response."""
        logger.warning("Using MockLLMClient - no actual API calls")

        # Return mock response based on prompt type
        if "job description" in user_prompt.lower():
            return json.dumps({
                "hard_skills": ["Python", "AWS", "Docker"],
                "soft_skills": ["Communication", "Leadership"],
                "qualifications": ["Bachelor's degree"],
                "experience_required": "3-5 years",
                "key_responsibilities": ["Develop software", "Lead projects"],
                "keywords": ["agile", "cloud", "API"],
                "culture_keywords": ["collaborative"],
                "nice_to_have": ["Master's degree"],
                "action_verbs": ["develop", "implement", "lead"],
                "company_name": "Tech Company",
                "job_title": "Software Engineer",
                "location": "Remote"
            })
        else:
            return """## Professional Summary
Experienced professional seeking new opportunities.

## Work Experience
Software Engineer | Company | 2020-Present
- Developed applications
- Led projects
"""
