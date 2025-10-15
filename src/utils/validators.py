"""Input validation utilities."""

from pathlib import Path
from typing import List


def validate_file_path(file_path: str, must_exist: bool = True) -> Path:
    """
    Validate a file path.

    Args:
        file_path: Path to validate.
        must_exist: If True, raise error if file doesn't exist.

    Returns:
        Path object if valid.

    Raises:
        FileNotFoundError: If file doesn't exist and must_exist is True.
        ValueError: If path is invalid.
    """
    if not file_path or not file_path.strip():
        raise ValueError("File path cannot be empty")

    path = Path(file_path)

    if must_exist and not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return path


def validate_output_format(format_str: str) -> str:
    """
    Validate output format string.

    Args:
        format_str: Format to validate (e.g., "markdown", "pdf", "txt").

    Returns:
        Lowercase format string if valid.

    Raises:
        ValueError: If format is not supported.
    """
    supported_formats = ["markdown", "md", "txt", "pdf"]

    format_lower = format_str.lower().strip()

    if format_lower not in supported_formats:
        raise ValueError(
            f"Unsupported format: {format_str}. "
            f"Supported formats: {', '.join(supported_formats)}"
        )

    return format_lower


def validate_file_size(file_path: str, max_size_mb: int = 10) -> bool:
    """
    Validate that a file is within size limits.

    Args:
        file_path: Path to the file.
        max_size_mb: Maximum allowed size in megabytes.

    Returns:
        True if file size is acceptable.

    Raises:
        ValueError: If file exceeds size limit.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    size_mb = path.stat().st_size / (1024 * 1024)

    if size_mb > max_size_mb:
        raise ValueError(
            f"File too large: {size_mb:.2f}MB (max: {max_size_mb}MB)"
        )

    return True


def validate_file_extension(file_path: str, allowed_extensions: List[str]) -> bool:
    """
    Validate file has an allowed extension.

    Args:
        file_path: Path to validate.
        allowed_extensions: List of allowed extensions (e.g., [".pdf", ".txt"]).

    Returns:
        True if extension is allowed.

    Raises:
        ValueError: If extension is not allowed.
    """
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension not in [ext.lower() for ext in allowed_extensions]:
        raise ValueError(
            f"Unsupported file extension: {extension}. "
            f"Allowed: {', '.join(allowed_extensions)}"
        )

    return True


def validate_job_description(job_desc: str, min_length: int = 50) -> bool:
    """
    Validate job description text.

    Args:
        job_desc: Job description to validate.
        min_length: Minimum required length.

    Returns:
        True if valid.

    Raises:
        ValueError: If job description is invalid.
    """
    if not job_desc or not job_desc.strip():
        raise ValueError("Job description cannot be empty")

    if len(job_desc.strip()) < min_length:
        raise ValueError(
            f"Job description too short: {len(job_desc.strip())} characters "
            f"(minimum: {min_length})"
        )

    return True


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize a filename by removing invalid characters.

    Args:
        filename: Filename to sanitize.
        max_length: Maximum allowed length.

    Returns:
        Sanitized filename.
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    sanitized = "".join(c if c not in invalid_chars else "_" for c in filename)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(". ")

    # Limit length
    if len(sanitized) > max_length:
        name, ext = sanitized.rsplit(".", 1) if "." in sanitized else (sanitized, "")
        max_name_length = max_length - len(ext) - 1
        sanitized = f"{name[:max_name_length]}.{ext}" if ext else name[:max_length]

    return sanitized or "untitled"
