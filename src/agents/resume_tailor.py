"""Resume Tailor Agent for optimizing resumes based on job requirements."""

from typing import List, Optional
from loguru import logger

from ..models.job_analysis import JobAnalysis
from ..models.resume_data import ResumeTailorResult


class ResumeTailorAgent:
    """
    Agent specialized in tailoring resumes to match job descriptions.

    This agent takes an original resume and job analysis, then optimizes the resume
    to highlight relevant experience and incorporate keywords naturally, while
    maintaining authenticity and never fabricating information.
    """

    SYSTEM_PROMPT = """You are a professional resume writer and career coach with over 15 years of expertise in ATS (Applicant Tracking Systems) optimization and modern resume best practices. Your mission is to help candidates present their EXISTING experience and skills in the best possible light for a specific job opportunity.

**CRITICAL RULES - YOU MUST FOLLOW THESE:**

1. **NEVER FABRICATE**: Never invent experience, skills, achievements, or qualifications that don't exist in the original resume
2. **MAINTAIN AUTHENTICITY**: Keep the candidate's authentic voice and writing style
3. **NO KEYWORD STUFFING**: Incorporate keywords naturally - they must fit contextually
4. **TRUTHFUL OPTIMIZATION**: Only emphasize, reframe, and reorder existing content
5. **QUANTIFY WHEN POSSIBLE**: If the original has numbers/metrics, maintain or highlight them
6. **ATS OPTIMIZATION**: Use clear headers, standard formatting, and relevant keywords
7. **CONCISE**: Keep the resume focused and impactful (1-2 pages ideal)

**YOUR PROCESS:**

1. **Analyze Original Resume**:
   - Carefully read every detail of the candidate's actual experience
   - Note their skills, achievements, and career progression
   - Identify their strengths and unique value proposition

2. **Review Target Job Requirements**:
   - Understand required skills, qualifications, and experience
   - Note key responsibilities and priorities
   - Identify critical keywords and phrases

3. **Find Authentic Matches**:
   - Match candidate's real experience with job requirements
   - Identify transferable skills from their background
   - Find relevant achievements that demonstrate required capabilities

4. **Optimize Presentation**:
   - Rewrite bullet points to emphasize relevant skills and achievements
   - Use action verbs from the job description where appropriate
   - Incorporate keywords naturally into existing experience descriptions
   - Reorder sections to prioritize most relevant experience
   - Strengthen the professional summary to align with the role

5. **Quality Checks**:
   - Ensure every statement is truthful and based on original resume
   - Verify keywords appear naturally in context
   - Confirm formatting is ATS-friendly
   - Check that the resume tells a compelling, coherent story

**FORMATTING GUIDELINES:**

- Use clear section headers: Professional Summary, Work Experience, Education, Skills, etc.
- Use strong action verbs: Led, Developed, Implemented, Optimized, Achieved, etc.
- Include specific metrics and results where available
- Use bullet points for readability
- Maintain consistent formatting throughout
- Keep professional summary concise (3-4 lines)

**OUTPUT:**

Return the complete tailored resume in clean Markdown format with:
- Clear section headers (use ##)
- Bullet points for experience items (use -)
- Professional, scannable formatting
- All content based on the original resume

Remember: Your goal is to help the candidate showcase their REAL experience in the most compelling way for this specific opportunity. You're not creating fiction - you're strategic storytelling with facts."""

    def __init__(self, model_client=None):
        """
        Initialize the Resume Tailor Agent.

        Args:
            model_client: The LLM client (from Strands SDK) for making API calls.
        """
        self.model_client = model_client
        logger.info("ResumeTailorAgent initialized")

    def tailor_resume(
        self,
        original_resume: str,
        job_analysis: JobAnalysis,
        job_description: Optional[str] = None
    ) -> str:
        """
        Tailor a resume to match job requirements while maintaining authenticity.

        Args:
            original_resume: The candidate's original resume text.
            job_analysis: Structured analysis of the target job.
            job_description: Optional full job description for context.

        Returns:
            Tailored resume as a string (Markdown format).

        Raises:
            ValueError: If inputs are invalid.
            Exception: For API or processing errors.
        """
        if len(original_resume.strip()) < 100:
            raise ValueError("Original resume is too short to process (minimum 100 characters)")

        logger.info("Tailoring resume to match job requirements...")
        logger.debug(f"Original resume length: {len(original_resume)} characters")
        logger.debug(f"Target skills: {len(job_analysis.hard_skills)} hard skills, "
                    f"{len(job_analysis.soft_skills)} soft skills")

        try:
            # Prepare the comprehensive prompt
            user_prompt = self._build_tailoring_prompt(original_resume, job_analysis, job_description)

            # Call the LLM
            if self.model_client:
                tailored_resume = self._call_llm(user_prompt)
            else:
                # Fallback for testing
                logger.warning("No model client provided, using mock tailoring")
                tailored_resume = self._mock_tailoring(original_resume, job_analysis)

            logger.success("Resume tailored successfully")
            logger.debug(f"Tailored resume length: {len(tailored_resume)} characters")

            return tailored_resume

        except Exception as e:
            logger.error(f"Error tailoring resume: {str(e)}")
            raise

    def _build_tailoring_prompt(
        self,
        original_resume: str,
        job_analysis: JobAnalysis,
        job_description: Optional[str] = None
    ) -> str:
        """
        Build the comprehensive prompt for resume tailoring.

        Args:
            original_resume: Original resume text.
            job_analysis: Job requirements and keywords.
            job_description: Optional full job description.

        Returns:
            Complete prompt string.
        """
        prompt_parts = [
            "# TASK: Tailor the following resume for a specific job opportunity\n",
            "## ORIGINAL RESUME (DO NOT CHANGE ANY FACTS):\n",
            "```",
            original_resume,
            "```\n",
            "## TARGET JOB ANALYSIS:\n",
        ]

        # Add job title if available
        if job_analysis.job_title:
            prompt_parts.append(f"**Job Title**: {job_analysis.job_title}\n")

        if job_analysis.company_name:
            prompt_parts.append(f"**Company**: {job_analysis.company_name}\n")

        # Add structured job requirements
        prompt_parts.extend([
            f"\n**Required Hard Skills**: {', '.join(job_analysis.hard_skills)}",
            f"\n**Required Soft Skills**: {', '.join(job_analysis.soft_skills)}",
            f"\n**Experience Level**: {job_analysis.experience_required}",
            f"\n**Key Responsibilities**: {', '.join(job_analysis.key_responsibilities[:5])}",
            f"\n**Important Keywords**: {', '.join(job_analysis.keywords[:15])}",
            f"\n**Action Verbs to Use**: {', '.join(job_analysis.action_verbs[:10])}",
        ])

        if job_analysis.qualifications:
            prompt_parts.append(f"\n**Required Qualifications**: {', '.join(job_analysis.qualifications)}")

        if job_analysis.culture_keywords:
            prompt_parts.append(f"\n**Company Culture**: {', '.join(job_analysis.culture_keywords)}")

        # Add full job description if provided
        if job_description:
            prompt_parts.extend([
                "\n\n## FULL JOB DESCRIPTION (for context):\n",
                "```",
                job_description[:2000],  # Truncate if too long
                "```\n"
            ])

        # Add instructions
        prompt_parts.extend([
            "\n## YOUR TASK:\n",
            "Tailor the original resume to highlight experiences and skills that match the job requirements.",
            "Remember: Only use information from the original resume. Do not fabricate anything.",
            "Incorporate the target keywords naturally. Use the suggested action verbs where appropriate.",
            "\nReturn ONLY the tailored resume in Markdown format with clear sections and bullet points.",
            "Do not include any explanations or comments - just the resume itself.\n",
            "\n**Tailored Resume:**\n"
        ])

        return "\n".join(prompt_parts)

    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the tailoring prompt.

        Args:
            prompt: The complete user prompt.

        Returns:
            The tailored resume as a string.
        """
        try:
            response = self.model_client.generate(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.7,  # Moderate temperature for creative but controlled rewriting
                max_tokens=3000
            )
            return response
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            raise

    def _mock_tailoring(self, original_resume: str, job_analysis: JobAnalysis) -> str:
        """
        Generate a mock tailored resume for testing.

        Args:
            original_resume: Original resume text.
            job_analysis: Job analysis data.

        Returns:
            Mock tailored resume.
        """
        # Simple mock that adds a summary section
        keywords_str = ", ".join(job_analysis.hard_skills[:5])
        job_title = job_analysis.job_title or "Target Position"

        mock_resume = f"""## Professional Summary

Experienced professional with expertise in {keywords_str}. Proven track record of delivering results in dynamic environments. Seeking to leverage skills and experience in the {job_title} role.

## {original_resume}

---
*Resume tailored for: {job_title}*
*Key skills highlighted: {keywords_str}*
"""
        return mock_resume

    def calculate_match_score(
        self,
        resume_text: str,
        job_analysis: JobAnalysis
    ) -> float:
        """
        Calculate how well a resume matches the job requirements.

        Args:
            resume_text: The resume text to analyze.
            job_analysis: Job requirements to match against.

        Returns:
            Match score as a percentage (0-100).
        """
        resume_lower = resume_text.lower()

        # Count matched skills
        all_required_items = (
            job_analysis.hard_skills +
            job_analysis.soft_skills +
            job_analysis.keywords
        )

        if not all_required_items:
            return 0.0

        matched_count = sum(
            1 for item in all_required_items
            if item.lower() in resume_lower
        )

        # Calculate percentage
        match_percentage = (matched_count / len(all_required_items)) * 100

        logger.info(f"Match score: {match_percentage:.1f}% ({matched_count}/{len(all_required_items)} keywords)")

        return round(match_percentage, 1)

    def identify_matched_keywords(
        self,
        resume_text: str,
        job_analysis: JobAnalysis
    ) -> List[str]:
        """
        Identify which keywords from the job appear in the resume.

        Args:
            resume_text: Resume text to search.
            job_analysis: Job analysis with keywords.

        Returns:
            List of matched keywords.
        """
        resume_lower = resume_text.lower()

        all_keywords = job_analysis.get_all_keywords()
        matched = [
            keyword for keyword in all_keywords
            if keyword.lower() in resume_lower
        ]

        return matched

    def generate_suggestions(
        self,
        original_resume: str,
        tailored_resume: str,
        job_analysis: JobAnalysis
    ) -> List[str]:
        """
        Generate suggestions for further improvements.

        Args:
            original_resume: Original resume text.
            tailored_resume: Tailored resume text.
            job_analysis: Job requirements.

        Returns:
            List of actionable suggestions.
        """
        suggestions = []

        # Check for missing critical skills
        critical_skills = job_analysis.hard_skills[:5]
        tailored_lower = tailored_resume.lower()

        missing_skills = [
            skill for skill in critical_skills
            if skill.lower() not in tailored_lower
        ]

        if missing_skills:
            suggestions.append(
                f"Consider adding experience with: {', '.join(missing_skills)} if applicable"
            )

        # Check for quantifiable metrics
        if not any(char.isdigit() for char in tailored_resume):
            suggestions.append(
                "Add quantifiable metrics and numbers to your achievements for greater impact"
            )

        # Check for action verbs
        action_verb_count = sum(
            1 for verb in job_analysis.action_verbs
            if verb.lower() in tailored_lower
        )

        if action_verb_count < 3:
            suggestions.append(
                f"Use more action verbs like: {', '.join(job_analysis.action_verbs[:5])}"
            )

        # Check for certifications
        if job_analysis.qualifications and "certification" in str(job_analysis.qualifications).lower():
            if "certif" not in tailored_lower:
                suggestions.append(
                    "Highlight any relevant certifications prominently"
                )

        return suggestions
