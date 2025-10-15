"""Main application logic for resume tailoring system."""

from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .agents.keyword_extractor import KeywordExtractorAgent
from .agents.resume_tailor import ResumeTailorAgent
from .tools.file_reader import FileReaderTool
from .tools.file_writer import FileWriterTool
from .models.job_analysis import JobAnalysis
from .models.resume_data import ResumeRequest, ResumeTailorResult
from .config.settings import get_settings
from .utils.logger import setup_logging
from .utils.validators import (
    validate_file_path,
    validate_output_format,
    validate_job_description
)

console = Console()


class ResumeTailoringSystem:
    """
    Main system orchestrating the resume tailoring workflow.

    Coordinates between KeywordExtractorAgent, ResumeTailorAgent, and file I/O tools
    to provide a complete resume tailoring solution.
    """

    def __init__(self, model_client=None, config=None):
        """
        Initialize the resume tailoring system.

        Args:
            model_client: Optional LLM client (Strands SDK).
            config: Optional settings override.
        """
        self.settings = config or get_settings()
        self.model_client = model_client

        # Initialize components
        self.keyword_extractor = KeywordExtractorAgent(model_client=model_client)
        self.resume_tailor = ResumeTailorAgent(model_client=model_client)
        self.file_reader = FileReaderTool()
        self.file_writer = FileWriterTool(output_directory=str(self.settings.get_output_path()))

        logger.info("ResumeTailoringSystem initialized")

    def process_resume(self, request: ResumeRequest) -> ResumeTailorResult:
        """
        Process a complete resume tailoring request.

        Args:
            request: ResumeRequest with all necessary inputs.

        Returns:
            ResumeTailorResult with tailored resume and metadata.
        """
        console.print("\n[bold blue]🚀 Starting Resume Tailoring Process[/bold blue]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            # Step 1: Read job description
            task1 = progress.add_task("[cyan]Reading job description...", total=None)
            job_description = self._load_job_description(request.job_description)
            progress.update(task1, completed=True)
            console.print("✓ Job description loaded\n")

            # Step 2: Analyze job description
            task2 = progress.add_task("[cyan]Analyzing job requirements...", total=None)
            job_analysis = self.keyword_extractor.analyze_job_description(job_description)
            progress.update(task2, completed=True)
            console.print(f"✓ Found {len(job_analysis.hard_skills)} hard skills, "
                        f"{len(job_analysis.soft_skills)} soft skills\n")

            # Step 3: Read original resume
            task3 = progress.add_task("[cyan]Reading original resume...", total=None)
            original_resume = self.file_reader.read_file(request.resume_file_path)
            progress.update(task3, completed=True)
            console.print("✓ Resume loaded\n")

            # Step 4: Tailor resume
            task4 = progress.add_task("[cyan]Tailoring resume to job requirements...", total=None)
            tailored_resume = self.resume_tailor.tailor_resume(
                original_resume=original_resume,
                job_analysis=job_analysis,
                job_description=job_description
            )
            progress.update(task4, completed=True)
            console.print("✓ Resume tailored successfully\n")

            # Step 5: Calculate match score
            match_score = None
            if request.calculate_match_score:
                task5 = progress.add_task("[cyan]Calculating match score...", total=None)
                match_score = self.resume_tailor.calculate_match_score(
                    tailored_resume, job_analysis
                )
                progress.update(task5, completed=True)
                console.print(f"✓ Match score: [bold green]{match_score}%[/bold green]\n")

            # Step 6: Identify matched keywords
            keywords_matched = self.resume_tailor.identify_matched_keywords(
                tailored_resume, job_analysis
            )

            # Step 7: Generate suggestions
            suggestions = self.resume_tailor.generate_suggestions(
                original_resume, tailored_resume, job_analysis
            )

            # Step 8: Save tailored resume
            task6 = progress.add_task("[cyan]Saving tailored resume...", total=None)
            output_path = self.file_writer.write_file(
                content=tailored_resume,
                output_format=request.output_format,
                custom_path=request.output_path,
                job_title=job_analysis.job_title
            )
            progress.update(task6, completed=True)
            console.print(f"✓ Saved to: [bold]{output_path}[/bold]\n")

            # Step 9: Generate comparison if requested
            comparison_path = None
            if request.show_comparison:
                task7 = progress.add_task("[cyan]Generating comparison...", total=None)
                comparison_path = self.file_writer.write_comparison(
                    original=original_resume,
                    tailored=tailored_resume
                )
                progress.update(task7, completed=True)
                console.print(f"✓ Comparison saved to: {comparison_path}\n")

        # Build result
        result = ResumeTailorResult(
            original_resume=original_resume,
            tailored_resume=tailored_resume,
            keywords_matched=keywords_matched,
            keywords_added=[],  # Could enhance this with diff analysis
            suggestions=suggestions,
            match_score=match_score,
            output_path=output_path,
            job_title=job_analysis.job_title,
            generated_at=datetime.now(),
            comparison=comparison_path
        )

        logger.success("Resume tailoring completed successfully")
        return result

    def _load_job_description(self, job_desc_input: str) -> str:
        """
        Load job description from string or file.

        Args:
            job_desc_input: Job description text or file path.

        Returns:
            Job description as string.
        """
        # Check if it's a file path
        try:
            path = Path(job_desc_input)
            if path.exists() and path.is_file():
                logger.info(f"Loading job description from file: {job_desc_input}")
                return self.file_reader.read_file(job_desc_input)
        except Exception:
            pass

        # Otherwise, treat as direct text
        validate_job_description(job_desc_input)
        return job_desc_input

    def tailor_resume(
        self,
        job_description: str,
        resume_path: str,
        output_format: str = "markdown",
        output_path: Optional[str] = None,
        show_comparison: bool = False
    ) -> ResumeTailorResult:
        """
        Simplified interface for tailoring a resume.

        Args:
            job_description: Job description text or file path.
            resume_path: Path to resume file.
            output_format: Output format (markdown, txt, pdf).
            output_path: Optional custom output path.
            show_comparison: Whether to generate comparison file.

        Returns:
            ResumeTailorResult with tailored resume and metrics.
        """
        request = ResumeRequest(
            job_description=job_description,
            resume_file_path=resume_path,
            output_format=output_format,
            output_path=output_path,
            show_comparison=show_comparison
        )

        return self.process_resume(request)

    def display_results(self, result: ResumeTailorResult) -> None:
        """
        Display results in a user-friendly format.

        Args:
            result: The tailoring result to display.
        """
        console.print("\n[bold green]✨ Resume Tailoring Complete![/bold green]\n")

        # Display summary
        console.print("[bold]Summary:[/bold]")
        console.print(f"  Job Title: {result.job_title or 'N/A'}")
        console.print(f"  Match Score: [bold]{result.match_score}%[/bold]" if result.match_score else "  Match Score: N/A")
        console.print(f"  Keywords Matched: {len(result.keywords_matched)}")
        console.print(f"  Output File: [bold]{result.output_path}[/bold]\n")

        # Display top matched keywords
        if result.keywords_matched:
            console.print("[bold]Top Matched Keywords:[/bold]")
            for keyword in result.keywords_matched[:10]:
                console.print(f"  • {keyword}")
            console.print()

        # Display suggestions
        if result.suggestions:
            console.print("[bold yellow]💡 Suggestions for Improvement:[/bold yellow]")
            for i, suggestion in enumerate(result.suggestions, 1):
                console.print(f"  {i}. {suggestion}")
            console.print()

        console.print("[bold green]🎉 Your tailored resume is ready![/bold green]\n")


def create_resume_tailor_system(
    model_provider: str = "bedrock",
    model_id: Optional[str] = None,
    use_mock: bool = False,
    **kwargs
) -> ResumeTailoringSystem:
    """
    Factory function to create a configured ResumeTailoringSystem.

    Args:
        model_provider: Model provider to use (bedrock, openai, anthropic).
        model_id: Specific model ID to use.
        use_mock: Use mock client for testing (no API calls).
        **kwargs: Additional configuration options.

    Returns:
        Configured ResumeTailoringSystem instance.
    """
    from .config.settings import get_settings
    from .llm.bedrock_client import BedrockClient, MockLLMClient

    settings = get_settings()

    # Override settings if provided
    if model_id:
        settings.model_id = model_id
    if model_provider:
        settings.model_provider = model_provider

    # Setup logging
    setup_logging(
        log_level=settings.log_level,
        log_file=settings.log_file
    )

    # Initialize model client
    if use_mock:
        logger.warning("Using MockLLMClient - no actual API calls will be made")
        model_client = MockLLMClient()
    elif model_provider == "bedrock":
        model_client = BedrockClient(
            model_id=settings.model_id,
            region=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    elif model_provider == "openai":
        from .llm.openai_client import OpenAIClient
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not set in .env file")
        # Use openai_model_id from settings, or the explicitly provided model_id
        openai_model = model_id if model_id else settings.openai_model_id
        model_client = OpenAIClient(
            api_key=settings.openai_api_key,
            model_id=openai_model
        )
    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

    system = ResumeTailoringSystem(
        model_client=model_client,
        config=settings
    )

    logger.info(f"Created ResumeTailoringSystem with provider: {model_provider}")

    return system


if __name__ == "__main__":
    # Example usage
    console.print("[bold]Resume Tailoring System - Example Usage[/bold]\n")

    # This would typically be called from CLI
    system = create_resume_tailor_system()

    console.print("System initialized. Use the CLI interface to process resumes.")
    console.print("Run: python -m src.cli --help")
