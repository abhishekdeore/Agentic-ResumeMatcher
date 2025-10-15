"""Tool for parsing and structuring resume content."""

import re
from typing import List, Dict, Optional, Tuple
from loguru import logger

from ..models.resume_data import ResumeSection, ParsedResume


class ResumeParserTool:
    """
    Tool for parsing resume text into structured sections.

    Intelligently identifies common resume sections and extracts content.
    """

    # Common section headers found in resumes
    SECTION_PATTERNS = [
        r"^(PROFESSIONAL\s+SUMMARY|SUMMARY|PROFILE|OBJECTIVE)",
        r"^(WORK\s+EXPERIENCE|EXPERIENCE|EMPLOYMENT\s+HISTORY|PROFESSIONAL\s+EXPERIENCE)",
        r"^(EDUCATION|ACADEMIC\s+BACKGROUND|ACADEMIC\s+QUALIFICATIONS)",
        r"^(SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|EXPERTISE)",
        r"^(CERTIFICATIONS|CERTIFICATES|PROFESSIONAL\s+CERTIFICATIONS)",
        r"^(PROJECTS|KEY\s+PROJECTS|NOTABLE\s+PROJECTS)",
        r"^(AWARDS|HONORS|ACHIEVEMENTS|ACCOMPLISHMENTS)",
        r"^(PUBLICATIONS|RESEARCH|PAPERS)",
        r"^(VOLUNTEER|VOLUNTEER\s+EXPERIENCE|COMMUNITY\s+SERVICE)",
        r"^(LANGUAGES|LANGUAGE\s+SKILLS)",
        r"^(INTERESTS|HOBBIES)",
        r"^(REFERENCES)",
    ]

    # Patterns for contact information
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'
    LINKEDIN_PATTERN = r'linkedin\.com/in/[\w-]+'

    def __init__(self):
        """Initialize the resume parser tool."""
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.SECTION_PATTERNS]

    def parse_resume(self, resume_text: str) -> ParsedResume:
        """
        Parse resume text into structured sections.

        Args:
            resume_text: Raw text of the resume.

        Returns:
            ParsedResume object with structured data.
        """
        logger.info("Parsing resume into structured sections")

        # Extract contact information
        contact_info = self._extract_contact_info(resume_text)

        # Split into sections
        sections = self._split_into_sections(resume_text)

        parsed_resume = ParsedResume(
            raw_text=resume_text,
            sections=sections,
            contact_info=contact_info
        )

        logger.success(f"Successfully parsed resume into {len(sections)} sections")
        return parsed_resume

    def _split_into_sections(self, text: str) -> List[ResumeSection]:
        """
        Split resume text into logical sections.

        Args:
            text: Resume text to split.

        Returns:
            List of ResumeSection objects.
        """
        lines = text.split("\n")
        sections: List[ResumeSection] = []
        current_section_name: Optional[str] = None
        current_content: List[str] = []

        for line in lines:
            stripped_line = line.strip()

            # Check if this line is a section header
            is_header, section_name = self._is_section_header(stripped_line)

            if is_header and section_name:
                # Save previous section if exists
                if current_section_name and current_content:
                    sections.append(self._create_section(current_section_name, current_content))

                # Start new section
                current_section_name = section_name
                current_content = []
            elif current_section_name:
                # Add line to current section
                if stripped_line:
                    current_content.append(line)

        # Add the last section
        if current_section_name and current_content:
            sections.append(self._create_section(current_section_name, current_content))

        # If no sections were identified, create a single section with all content
        if not sections:
            sections.append(
                ResumeSection(
                    section_name="Full Resume",
                    content=text,
                    bullet_points=self._extract_bullet_points(text)
                )
            )

        return sections

    def _is_section_header(self, line: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a line is a section header.

        Args:
            line: Line to check.

        Returns:
            Tuple of (is_header, normalized_section_name).
        """
        # Check against known patterns
        for pattern in self.compiled_patterns:
            if pattern.match(line):
                # Normalize the section name
                normalized = self._normalize_section_name(line)
                return True, normalized

        # Additional heuristics for headers
        # Headers are typically short, uppercase or title case, and may end with colon
        if len(line) < 50 and (line.isupper() or line.istitle()):
            if ":" in line:
                line = line.rstrip(":")
            return True, line.strip()

        return False, None

    def _normalize_section_name(self, header: str) -> str:
        """
        Normalize section names to standard format.

        Args:
            header: Raw section header text.

        Returns:
            Normalized section name.
        """
        header = header.strip().rstrip(":").upper()

        # Map variations to standard names
        if "SUMMARY" in header or "PROFILE" in header or "OBJECTIVE" in header:
            return "Professional Summary"
        elif "EXPERIENCE" in header or "EMPLOYMENT" in header:
            return "Work Experience"
        elif "EDUCATION" in header or "ACADEMIC" in header:
            return "Education"
        elif "SKILL" in header or "COMPETENC" in header or "EXPERTISE" in header:
            return "Skills"
        elif "CERTIFICATION" in header or "CERTIFICATE" in header:
            return "Certifications"
        elif "PROJECT" in header:
            return "Projects"
        elif "AWARD" in header or "HONOR" in header or "ACHIEVEMENT" in header:
            return "Awards & Achievements"
        elif "PUBLICATION" in header or "RESEARCH" in header:
            return "Publications"
        elif "VOLUNTEER" in header or "COMMUNITY" in header:
            return "Volunteer Experience"
        elif "LANGUAGE" in header:
            return "Languages"
        elif "INTEREST" in header or "HOBBIES" in header:
            return "Interests"
        elif "REFERENCE" in header:
            return "References"
        else:
            return header.title()

    def _create_section(self, section_name: str, content_lines: List[str]) -> ResumeSection:
        """
        Create a ResumeSection from name and content lines.

        Args:
            section_name: Name of the section.
            content_lines: Lines of content.

        Returns:
            ResumeSection object.
        """
        content = "\n".join(content_lines)
        bullet_points = self._extract_bullet_points(content)

        return ResumeSection(
            section_name=section_name,
            content=content,
            bullet_points=bullet_points
        )

    def _extract_bullet_points(self, text: str) -> List[str]:
        """
        Extract bullet points from text.

        Args:
            text: Text to extract bullets from.

        Returns:
            List of bullet point strings.
        """
        bullet_patterns = [
            r'^\s*[•●■▪▸►→-]\s+(.+)$',  # Various bullet symbols
            r'^\s*\*\s+(.+)$',            # Asterisk bullets
            r'^\s*\d+\.\s+(.+)$',         # Numbered lists
        ]

        bullets = []
        lines = text.split("\n")

        for line in lines:
            for pattern in bullet_patterns:
                match = re.match(pattern, line)
                if match:
                    bullets.append(match.group(1).strip())
                    break

        return bullets

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information from resume text.

        Args:
            text: Resume text.

        Returns:
            Dictionary of contact information.
        """
        contact_info = {}

        # Extract email
        email_matches = re.findall(self.EMAIL_PATTERN, text)
        if email_matches:
            contact_info["email"] = email_matches[0]

        # Extract phone
        phone_matches = re.findall(self.PHONE_PATTERN, text)
        if phone_matches:
            # Clean up phone number
            phone = "".join(phone_matches[0]) if isinstance(phone_matches[0], tuple) else phone_matches[0]
            contact_info["phone"] = phone

        # Extract LinkedIn
        linkedin_matches = re.findall(self.LINKEDIN_PATTERN, text, re.IGNORECASE)
        if linkedin_matches:
            contact_info["linkedin"] = f"https://{linkedin_matches[0]}"

        # Extract URLs
        url_matches = re.findall(self.URL_PATTERN, text)
        if url_matches:
            # Filter out LinkedIn (already captured)
            other_urls = [url for url in url_matches if "linkedin.com" not in url.lower()]
            if other_urls:
                contact_info["website"] = other_urls[0]

        # Try to extract name (typically in the first few lines)
        lines = text.split("\n")[:5]
        for line in lines:
            line = line.strip()
            # Name heuristic: Short line (< 50 chars), title case, not a section header
            if line and len(line) < 50 and not any(char.isdigit() for char in line):
                if line.istitle() or (line.isupper() and len(line.split()) <= 4):
                    # Check it's not an email or phone
                    if "@" not in line and not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line):
                        contact_info["name"] = line
                        break

        logger.debug(f"Extracted contact info: {list(contact_info.keys())}")
        return contact_info

    def extract_keywords(self, text: str) -> List[str]:
        """
        Extract potential keywords from text (skills, technologies, etc.).

        Args:
            text: Text to extract keywords from.

        Returns:
            List of potential keywords.
        """
        # This is a simple implementation - could be enhanced with NLP
        # Common technical skills and keywords
        common_keywords = [
            "Python", "Java", "JavaScript", "C++", "SQL", "AWS", "Azure", "GCP",
            "Docker", "Kubernetes", "CI/CD", "Git", "Agile", "Scrum", "REST",
            "API", "Machine Learning", "ML", "AI", "Data Science", "TensorFlow",
            "PyTorch", "React", "Angular", "Vue", "Node.js", "Django", "Flask",
            "MongoDB", "PostgreSQL", "MySQL", "Redis", "Kafka", "Microservices",
            "Leadership", "Communication", "Team", "Management", "Project Management"
        ]

        found_keywords = []
        text_lower = text.lower()

        for keyword in common_keywords:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)

        return found_keywords
