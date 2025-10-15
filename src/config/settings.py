"""Application configuration using pydantic-settings."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Configuration can be provided via:
    1. Environment variables
    2. .env file
    3. Default values
    """

    # Model Configuration
    model_provider: str = "bedrock"
    model_id: str = "us.anthropic.claude-sonnet-4-20250514-v1:0"
    aws_region: str = "us-west-2"
    temperature: float = 0.7
    max_tokens: int = 4000

    # AWS Credentials (for Bedrock)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # Alternative Model Providers
    openai_api_key: Optional[str] = None
    openai_model_id: str = "gpt-4"
    anthropic_api_key: Optional[str] = None

    # Application Settings
    output_directory: str = "./output"
    log_level: str = "INFO"
    log_file: Optional[str] = None

    # Resume Processing
    max_resume_size_mb: int = 10
    supported_formats: list = [".txt", ".pdf", ".docx", ".doc"]

    # Performance
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def validate_aws_credentials(self) -> bool:
        """
        Check if AWS credentials are configured.

        Returns:
            True if credentials are available, False otherwise.
        """
        if self.model_provider != "bedrock":
            return True

        return bool(self.aws_access_key_id and self.aws_secret_access_key)

    def get_output_path(self) -> Path:
        """
        Get the output directory as a Path object.

        Returns:
            Path object for the output directory.
        """
        path = Path(self.output_directory)
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_model_config(self) -> dict:
        """
        Get model configuration as a dictionary.

        Returns:
            Dictionary with model settings.
        """
        return {
            "provider": self.model_provider,
            "model_id": self.model_id,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "region": self.aws_region if self.model_provider == "bedrock" else None,
        }


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern).

    Returns:
        Settings object with current configuration.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing).

    Returns:
        Fresh Settings object.
    """
    global _settings
    _settings = Settings()
    return _settings
