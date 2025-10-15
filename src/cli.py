"""Command-line interface for the Resume Tailoring System."""

import click
from pathlib import Path
from rich.console import Console
from loguru import logger

from .main import create_resume_tailor_system
from .models.resume_data import ResumeRequest
from .config.settings import get_settings
from .utils.logger import setup_logging

console = Console()


@click.group()
@click.option('--log-level', default='INFO', help='Logging level (DEBUG, INFO, WARNING, ERROR)')
@click.option('--log-file', default=None, help='Optional log file path')
@click.pass_context
def cli(ctx, log_level, log_file):
    """
    Agentic Resume Matcher - AI-powered resume tailoring system.

    Tailor your resume to specific job descriptions using AI agents.
    """
    ctx.ensure_object(dict)
    ctx.obj['log_level'] = log_level
    ctx.obj['log_file'] = log_file

    # Setup logging
    setup_logging(log_level=log_level, log_file=log_file)


@cli.command()
@click.option('--job-description', '-j', required=True, help='Job description text or file path')
@click.option('--resume', '-r', required=True, help='Path to your resume file (.txt, .pdf, .docx)')
@click.option('--output', '-o', default=None, help='Custom output file path')
@click.option('--format', '-f', default='markdown', type=click.Choice(['markdown', 'md', 'txt', 'pdf'], case_sensitive=False), help='Output format')
@click.option('--comparison', is_flag=True, help='Generate side-by-side comparison')
@click.option('--model-provider', default='bedrock', type=click.Choice(['bedrock', 'openai', 'anthropic'], case_sensitive=False), help='LLM provider to use')
@click.option('--model-id', default=None, help='Specific model ID to use')
@click.option('--mock', is_flag=True, help='Use mock LLM (no API calls, for testing)')
@click.pass_context
def tailor(ctx, job_description, resume, output, format, comparison, model_provider, model_id, mock):
    """
    Tailor a resume to a specific job description.

    Example:
        python -m src.cli tailor -j job.txt -r resume.pdf -f markdown
    """
    try:
        console.print("\n[bold cyan]Agentic Resume Matcher[/bold cyan]")
        console.print("AI-Powered Resume Tailoring\n")

        # Create system
        system = create_resume_tailor_system(
            model_provider=model_provider,
            model_id=model_id,
            use_mock=mock
        )

        # Create request
        request = ResumeRequest(
            job_description=job_description,
            resume_file_path=resume,
            output_format=format,
            output_path=output,
            show_comparison=comparison
        )

        # Process
        result = system.process_resume(request)

        # Display results
        system.display_results(result)

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}\n")
        logger.exception("Error during resume tailoring")
        raise click.Abort()


@cli.command()
@click.option('--job-description', '-j', required=True, help='Job description text or file path')
@click.pass_context
def analyze(ctx, job_description):
    """
    Analyze a job description and extract keywords.

    Example:
        python -m src.cli analyze -j job.txt
    """
    try:
        from .agents.keyword_extractor import KeywordExtractorAgent
        from .tools.file_reader import FileReaderTool

        console.print("\n[bold cyan]Job Description Analysis[/bold cyan]\n")

        # Load job description
        try:
            path = Path(job_description)
            if path.exists():
                reader = FileReaderTool()
                job_desc_text = reader.read_file(job_description)
            else:
                job_desc_text = job_description
        except Exception:
            job_desc_text = job_description

        # Analyze
        extractor = KeywordExtractorAgent()
        analysis = extractor.analyze_job_description(job_desc_text)

        # Display results
        console.print("[bold]Job Analysis Results:[/bold]\n")

        if analysis.job_title:
            console.print(f"[bold]Job Title:[/bold] {analysis.job_title}")
        if analysis.company_name:
            console.print(f"[bold]Company:[/bold] {analysis.company_name}")
        if analysis.location:
            console.print(f"[bold]Location:[/bold] {analysis.location}")

        console.print(f"\n[bold]Experience Required:[/bold] {analysis.experience_required}")

        console.print(f"\n[bold]Hard Skills ({len(analysis.hard_skills)}):[/bold]")
        for skill in analysis.hard_skills:
            console.print(f"  • {skill}")

        console.print(f"\n[bold]Soft Skills ({len(analysis.soft_skills)}):[/bold]")
        for skill in analysis.soft_skills:
            console.print(f"  • {skill}")

        if analysis.qualifications:
            console.print(f"\n[bold]Required Qualifications:[/bold]")
            for qual in analysis.qualifications:
                console.print(f"  • {qual}")

        if analysis.key_responsibilities:
            console.print(f"\n[bold]Key Responsibilities:[/bold]")
            for resp in analysis.key_responsibilities[:5]:
                console.print(f"  • {resp}")

        console.print(f"\n[bold]Keywords ({len(analysis.keywords)}):[/bold]")
        console.print(f"  {', '.join(analysis.keywords[:15])}")

        console.print("\n✓ Analysis complete\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}\n")
        logger.exception("Error during job analysis")
        raise click.Abort()


@cli.command()
@click.option('--resume', '-r', required=True, help='Path to resume file')
@click.option('--format', '-f', default='markdown', type=click.Choice(['markdown', 'txt'], case_sensitive=False), help='Output format')
@click.pass_context
def parse(ctx, resume, format):
    """
    Parse a resume and display its structure.

    Example:
        python -m src.cli parse -r resume.pdf
    """
    try:
        from .tools.file_reader import FileReaderTool
        from .tools.parser import ResumeParserTool

        console.print("\n[bold cyan]Resume Parser[/bold cyan]\n")

        # Read resume
        reader = FileReaderTool()
        resume_text = reader.read_file(resume)

        # Parse
        parser = ResumeParserTool()
        parsed = parser.parse_resume(resume_text)

        # Display
        console.print(f"[bold]Resume Sections Found: {len(parsed.sections)}[/bold]\n")

        if parsed.contact_info:
            console.print("[bold]Contact Information:[/bold]")
            for key, value in parsed.contact_info.items():
                console.print(f"  {key.title()}: {value}")
            console.print()

        for section in parsed.sections:
            console.print(f"[bold cyan]{section.section_name}[/bold cyan]")
            console.print(f"  Length: {len(section.content)} characters")
            if section.bullet_points:
                console.print(f"  Bullet points: {len(section.bullet_points)}")
            console.print()

        console.print("✓ Parsing complete\n")

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}\n")
        logger.exception("Error parsing resume")
        raise click.Abort()


@cli.command()
def config():
    """Display current configuration."""
    try:
        settings = get_settings()

        console.print("\n[bold cyan]Current Configuration[/bold cyan]\n")

        console.print("[bold]Model Settings:[/bold]")
        console.print(f"  Provider: {settings.model_provider}")
        console.print(f"  Model ID: {settings.model_id}")
        console.print(f"  Temperature: {settings.temperature}")
        console.print(f"  Max Tokens: {settings.max_tokens}")

        console.print("\n[bold]Application Settings:[/bold]")
        console.print(f"  Output Directory: {settings.output_directory}")
        console.print(f"  Log Level: {settings.log_level}")

        console.print("\n[bold]AWS Settings (Bedrock):[/bold]")
        console.print(f"  Region: {settings.aws_region}")
        console.print(f"  Credentials Configured: {settings.validate_aws_credentials()}")

        console.print()

    except Exception as e:
        console.print(f"\n[bold red]❌ Error:[/bold red] {str(e)}\n")
        raise click.Abort()


@cli.command()
def version():
    """Display version information."""
    from . import __version__
    console.print(f"\n[bold]Agentic Resume Matcher[/bold] v{__version__}\n")


if __name__ == '__main__':
    cli(obj={})
