"""Tool for writing tailored resumes to various file formats."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT
from loguru import logger


class FileWriterTool:
    """
    Tool for writing tailored resumes to various output formats.

    Supports markdown, plain text, and PDF formats with professional formatting.
    """

    SUPPORTED_FORMATS = ["markdown", "md", "txt", "pdf"]

    def __init__(self, output_directory: str = "./output"):
        """
        Initialize the file writer tool.

        Args:
            output_directory: Directory where output files will be saved.
        """
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"FileWriterTool initialized with output directory: {self.output_directory}")

    def write_file(
        self,
        content: str,
        output_format: str = "markdown",
        custom_path: Optional[str] = None,
        job_title: Optional[str] = None,
    ) -> str:
        """
        Write content to a file in the specified format.

        Args:
            content: The resume content to write.
            output_format: Format to write (markdown, txt, pdf).
            custom_path: Custom output file path (optional).
            job_title: Job title for metadata (optional).

        Returns:
            Path to the created file.

        Raises:
            ValueError: If the output format is unsupported.
        """
        output_format = output_format.lower()

        if output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported output format: {output_format}. "
                f"Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        # Determine output path
        if custom_path:
            output_path = Path(custom_path)
        else:
            output_path = self._generate_output_path(output_format, job_title)

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Writing tailored resume to: {output_path}")

        # Write based on format
        try:
            if output_format == "pdf":
                self._write_pdf(content, output_path, job_title)
            else:
                self._write_text(content, output_path, output_format)

            logger.success(f"Successfully wrote file: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"Error writing file {output_path}: {str(e)}")
            raise

    def _generate_output_path(self, output_format: str, job_title: Optional[str] = None) -> Path:
        """
        Generate an output file path with timestamp.

        Args:
            output_format: The output format extension.
            job_title: Optional job title for filename.

        Returns:
            Path object for the output file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if job_title:
            # Sanitize job title for filename
            safe_title = "".join(c if c.isalnum() or c in (" ", "-", "_") else "" for c in job_title)
            safe_title = safe_title.replace(" ", "_")[:50]  # Limit length
            filename = f"tailored_resume_{safe_title}_{timestamp}"
        else:
            filename = f"tailored_resume_{timestamp}"

        # Normalize extension
        ext = "md" if output_format == "markdown" else output_format
        return self.output_directory / f"{filename}.{ext}"

    def _write_text(self, content: str, output_path: Path, output_format: str) -> None:
        """
        Write content to a text or markdown file.

        Args:
            content: Content to write.
            output_path: Path to write to.
            output_format: Format type (for potential future formatting differences).
        """
        # Add metadata header for markdown
        if output_format in ["markdown", "md"]:
            metadata = self._generate_metadata_header()
            full_content = f"{metadata}\n\n{content}"
        else:
            full_content = content

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_content)

    def _write_pdf(self, content: str, output_path: Path, job_title: Optional[str] = None) -> None:
        """
        Write content to a PDF file with professional formatting.

        Args:
            content: Markdown or plain text content to convert to PDF.
            output_path: Path to write the PDF.
            job_title: Optional job title for metadata.
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=letter,
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch,
            )

            # Define styles
            styles = getSampleStyleSheet()
            styles.add(
                ParagraphStyle(
                    name="CustomBody",
                    parent=styles["BodyText"],
                    fontSize=10,
                    leading=14,
                    alignment=TA_LEFT,
                )
            )
            styles.add(
                ParagraphStyle(
                    name="CustomHeading",
                    parent=styles["Heading1"],
                    fontSize=14,
                    leading=18,
                    spaceAfter=12,
                    textColor="darkblue",
                )
            )

            # Build document elements
            story = []

            # Parse content into paragraphs and headings
            lines = content.split("\n")
            for line in lines:
                line = line.strip()

                if not line:
                    story.append(Spacer(1, 0.1 * inch))
                    continue

                # Detect markdown headers
                if line.startswith("# "):
                    text = line[2:].strip()
                    para = Paragraph(text, styles["CustomHeading"])
                    story.append(para)
                    story.append(Spacer(1, 0.1 * inch))
                elif line.startswith("## "):
                    text = line[3:].strip()
                    para = Paragraph(f"<b>{text}</b>", styles["CustomBody"])
                    story.append(para)
                    story.append(Spacer(1, 0.05 * inch))
                elif line.startswith("- ") or line.startswith("* "):
                    text = line[2:].strip()
                    para = Paragraph(f"• {text}", styles["CustomBody"])
                    story.append(para)
                else:
                    # Regular paragraph - escape special characters
                    text = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    para = Paragraph(text, styles["CustomBody"])
                    story.append(para)

            # Build PDF
            doc.build(story)

        except Exception as e:
            logger.error(f"Error creating PDF: {str(e)}")
            raise ValueError(f"Failed to create PDF: {str(e)}")

    def _generate_metadata_header(self) -> str:
        """
        Generate metadata header for markdown files.

        Returns:
            Formatted metadata string.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"<!-- Generated by Agentic Resume Matcher on {timestamp} -->"

    def write_comparison(
        self, original: str, tailored: str, output_path: Optional[str] = None
    ) -> str:
        """
        Write a side-by-side comparison of original and tailored resumes.

        Args:
            original: Original resume content.
            tailored: Tailored resume content.
            output_path: Custom output path (optional).

        Returns:
            Path to the comparison file.
        """
        comparison_content = self._format_comparison(original, tailored)

        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_directory / f"comparison_{timestamp}.md"
        else:
            output_path = Path(output_path)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(comparison_content)

        logger.info(f"Comparison written to: {output_path}")
        return str(output_path)

    def _format_comparison(self, original: str, tailored: str) -> str:
        """
        Format original and tailored resumes for side-by-side comparison.

        Args:
            original: Original resume content.
            tailored: Tailored resume content.

        Returns:
            Formatted comparison in markdown.
        """
        lines = [
            "# Resume Comparison",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "---",
            "",
            "## Original Resume",
            "",
            original,
            "",
            "---",
            "",
            "## Tailored Resume",
            "",
            tailored,
            "",
        ]
        return "\n".join(lines)
