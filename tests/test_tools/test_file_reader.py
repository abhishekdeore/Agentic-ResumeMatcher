"""Tests for file reader tool."""

import pytest
from pathlib import Path
from src.tools.file_reader import FileReaderTool


@pytest.fixture
def file_reader():
    """Create a FileReaderTool instance."""
    return FileReaderTool()


@pytest.fixture
def sample_text_file(tmp_path):
    """Create a temporary text file for testing."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("This is a test resume.\nWith multiple lines.")
    return str(file_path)


def test_read_text_file(file_reader, sample_text_file):
    """Test reading a plain text file."""
    content = file_reader.read_file(sample_text_file)
    assert "This is a test resume" in content
    assert len(content) > 0


def test_file_not_found(file_reader):
    """Test error handling for non-existent files."""
    with pytest.raises(FileNotFoundError):
        file_reader.read_file("nonexistent_file.txt")


def test_unsupported_format(file_reader, tmp_path):
    """Test error handling for unsupported file formats."""
    unsupported_file = tmp_path / "test.xyz"
    unsupported_file.write_text("content")

    with pytest.raises(ValueError, match="Unsupported file format"):
        file_reader.read_file(str(unsupported_file))


def test_empty_file_error(file_reader, tmp_path):
    """Test error handling for empty files."""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")

    with pytest.raises(ValueError, match="empty"):
        file_reader.read_file(str(empty_file))


def test_validate_file(file_reader, sample_text_file):
    """Test file validation method."""
    assert file_reader.validate_file(sample_text_file) is True
    assert file_reader.validate_file("nonexistent.txt") is False


def test_get_file_info(file_reader, sample_text_file):
    """Test getting file metadata."""
    info = file_reader.get_file_info(sample_text_file)

    assert info["exists"] is True
    assert info["extension"] == ".txt"
    assert info["is_supported"] is True
    assert info["size_bytes"] > 0
