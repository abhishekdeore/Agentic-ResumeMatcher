"""Example of using the Resume Tailoring System via Python code."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import create_resume_tailor_system
from src.models.resume_data import ResumeRequest


def example_basic_usage():
    """Basic example of tailoring a resume."""
    print("=== Basic Resume Tailoring Example ===\n")

    # Create the system
    system = create_resume_tailor_system(model_provider="bedrock")

    # Define inputs
    job_description = """
    Senior Software Engineer - Cloud Infrastructure

    We're looking for an experienced Software Engineer to join our cloud infrastructure team.

    Required Skills:
    - 5+ years of software development experience
    - Strong Python and Go programming skills
    - Experience with AWS (EC2, S3, Lambda, RDS)
    - Docker and Kubernetes expertise
    - CI/CD pipeline development
    - Infrastructure as Code (Terraform, CloudFormation)

    Responsibilities:
    - Design and implement scalable cloud infrastructure
    - Build and maintain CI/CD pipelines
    - Optimize system performance and reliability
    - Mentor junior engineers
    - Collaborate with cross-functional teams

    Nice to have:
    - Experience with monitoring tools (Datadog, CloudWatch)
    - Background in security best practices
    - Open source contributions
    """

    resume_path = "tests/fixtures/sample_resume.txt"

    # Tailor the resume
    try:
        result = system.tailor_resume(
            job_description=job_description,
            resume_path=resume_path,
            output_format="markdown",
            show_comparison=False
        )

        # Display results
        system.display_results(result)

        print(f"\nTailored resume saved to: {result.output_path}")
        print(f"Match score: {result.match_score}%")

    except Exception as e:
        print(f"Error: {str(e)}")


def example_with_request_object():
    """Example using ResumeRequest object for more control."""
    print("\n=== Advanced Usage with ResumeRequest ===\n")

    system = create_resume_tailor_system()

    # Create a detailed request
    request = ResumeRequest(
        job_description="tests/fixtures/sample_job_description.txt",
        resume_file_path="tests/fixtures/sample_resume.pdf",
        output_format="pdf",
        output_path="./output/my_tailored_resume.pdf",
        show_comparison=True,
        calculate_match_score=True
    )

    try:
        result = system.process_resume(request)

        print(f"✓ Resume tailored successfully")
        print(f"✓ Match score: {result.match_score}%")
        print(f"✓ Matched {len(result.keywords_matched)} keywords")
        print(f"✓ Output: {result.output_path}")

        if result.suggestions:
            print("\nSuggestions:")
            for i, suggestion in enumerate(result.suggestions, 1):
                print(f"  {i}. {suggestion}")

    except Exception as e:
        print(f"Error: {str(e)}")


def example_analyze_job_only():
    """Example of analyzing a job description without tailoring."""
    print("\n=== Job Description Analysis Example ===\n")

    from src.agents.keyword_extractor import KeywordExtractorAgent

    extractor = KeywordExtractorAgent()

    job_description = """
    Data Scientist - Machine Learning

    Join our AI team to build cutting-edge ML models.

    Requirements:
    - PhD or Master's in Computer Science, Statistics, or related field
    - 3+ years of ML experience
    - Strong Python skills (NumPy, Pandas, Scikit-learn, TensorFlow/PyTorch)
    - Experience with NLP and computer vision
    - SQL and data analysis expertise

    You'll be responsible for:
    - Developing and deploying ML models
    - Conducting experiments and A/B testing
    - Collaborating with product teams
    - Presenting findings to stakeholders
    """

    try:
        analysis = extractor.analyze_job_description(job_description)

        print(f"Job Title: {analysis.job_title}")
        print(f"Experience Required: {analysis.experience_required}")
        print(f"\nHard Skills: {', '.join(analysis.hard_skills)}")
        print(f"Soft Skills: {', '.join(analysis.soft_skills)}")
        print(f"Keywords: {', '.join(analysis.keywords[:10])}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Run examples
    print("Resume Tailoring System - Python API Examples\n")
    print("=" * 60)

    # Uncomment to run specific examples:
    example_analyze_job_only()
    # example_basic_usage()
    # example_with_request_object()
