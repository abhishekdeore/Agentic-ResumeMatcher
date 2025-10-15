"""Tests for KeywordExtractorAgent."""

import pytest
from src.agents.keyword_extractor import KeywordExtractorAgent
from src.models.job_analysis import JobAnalysis


@pytest.fixture
def extractor():
    """Create a KeywordExtractorAgent instance."""
    return KeywordExtractorAgent()


@pytest.fixture
def sample_job_description():
    """Sample job description for testing."""
    return """
    Senior Software Engineer

    We're looking for an experienced engineer with 5+ years of Python experience.
    Must have strong knowledge of AWS, Docker, and Kubernetes.
    Excellent communication and leadership skills required.

    Responsibilities:
    - Lead technical projects
    - Mentor junior developers
    - Design scalable systems

    Qualifications:
    - Bachelor's in Computer Science
    - AWS Certification preferred
    """


def test_analyze_short_job_description(extractor):
    """Test error handling for too-short job descriptions."""
    with pytest.raises(ValueError, match="too short"):
        extractor.analyze_job_description("Short text")


def test_analyze_job_description_structure(extractor, sample_job_description):
    """Test that analysis returns proper structure."""
    result = extractor.analyze_job_description(sample_job_description)

    assert isinstance(result, JobAnalysis)
    assert isinstance(result.hard_skills, list)
    assert isinstance(result.soft_skills, list)
    assert isinstance(result.experience_required, str)


def test_mock_analysis_extracts_keywords(extractor, sample_job_description):
    """Test mock analysis extracts basic keywords."""
    result = extractor.analyze_job_description(sample_job_description)

    # Should extract some skills even in mock mode
    assert len(result.hard_skills) > 0 or len(result.soft_skills) > 0
    assert result.experience_required is not None
