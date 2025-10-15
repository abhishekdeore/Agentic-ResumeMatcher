"""Keyword Extractor Agent for analyzing job descriptions."""

import json
from typing import Optional
from loguru import logger

from ..models.job_analysis import JobAnalysis


class KeywordExtractorAgent:
    """
    Agent specialized in analyzing job descriptions and extracting key information.

    This agent uses an LLM to thoroughly analyze job postings and extract:
    - Required hard and soft skills
    - Qualifications and certifications
    - Experience requirements
    - Key responsibilities
    - Industry keywords and cultural indicators
    """

    SYSTEM_PROMPT = """You are an expert recruiter and job description analyzer with 15+ years of experience in talent acquisition and HR. Your task is to thoroughly analyze job descriptions and extract ALL relevant information that would help a candidate tailor their resume.

Your analysis must be comprehensive, precise, and structured. You understand how ATS (Applicant Tracking Systems) work and know exactly what keywords and phrases recruiters look for.

Extract and categorize the following information:

1. **Hard Skills**: Technical skills, tools, technologies, programming languages, software, platforms
2. **Soft Skills**: Leadership, communication, teamwork, problem-solving, creativity, etc.
3. **Qualifications**: Required degrees, certifications, licenses, credentials
4. **Experience Level**: Years of experience, seniority level, career stage
5. **Key Responsibilities**: Main duties, what you'll be doing day-to-day
6. **Industry Keywords**: Domain-specific terminology, buzzwords, technical jargon
7. **Culture Keywords**: Company values, work environment indicators, cultural fit markers
8. **Nice-to-Have**: Optional skills, preferred qualifications, bonus points
9. **Action Verbs**: Strong action words used in the job description that should appear in the resume

**Analysis Guidelines:**
- Be thorough but precise - extract everything relevant
- Provide context for ambiguous terms
- Identify both explicit and implicit requirements
- Note the priority/importance of different skills when apparent
- Extract acronyms and their full forms
- Identify must-haves vs. nice-to-haves

**Output Format:**
Return your analysis as a valid JSON object with these exact keys:
- hard_skills (array of strings)
- soft_skills (array of strings)
- qualifications (array of strings)
- experience_required (string)
- key_responsibilities (array of strings)
- keywords (array of strings)
- culture_keywords (array of strings)
- nice_to_have (array of strings)
- action_verbs (array of strings)
- company_name (string or null)
- job_title (string or null)
- location (string or null)

Be systematic and thorough. This analysis will directly impact a candidate's success."""

    def __init__(self, model_client=None):
        """
        Initialize the Keyword Extractor Agent.

        Args:
            model_client: The LLM client (from Strands SDK) for making API calls.
        """
        self.model_client = model_client
        logger.info("KeywordExtractorAgent initialized")

    def analyze_job_description(self, job_description: str) -> JobAnalysis:
        """
        Analyze a job description and extract structured information.

        Args:
            job_description: The full text of the job description.

        Returns:
            JobAnalysis object with all extracted information.

        Raises:
            ValueError: If the job description is too short or invalid.
            Exception: For API or parsing errors.
        """
        if len(job_description.strip()) < 50:
            raise ValueError("Job description is too short to analyze (minimum 50 characters)")

        logger.info("Analyzing job description...")
        logger.debug(f"Job description length: {len(job_description)} characters")

        try:
            # Prepare the prompt
            user_prompt = f"""Analyze the following job description and extract all relevant information. Return ONLY a valid JSON object with no additional text or markdown formatting.

Job Description:
{job_description}

Return the JSON analysis:"""

            # Call the LLM
            if self.model_client:
                response = self._call_llm(user_prompt)
            else:
                # Fallback for testing without a model
                logger.warning("No model client provided, using mock analysis")
                response = self._mock_analysis(job_description)

            # Parse the response
            analysis = self._parse_response(response)

            logger.success(f"Job description analyzed successfully. Found {len(analysis.hard_skills)} hard skills, "
                         f"{len(analysis.soft_skills)} soft skills, {len(analysis.key_responsibilities)} responsibilities")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            raise

    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the system and user prompts.

        Args:
            prompt: The user prompt to send.

        Returns:
            The LLM's response as a string.
        """
        try:
            response = self.model_client.generate(
                system_prompt=self.SYSTEM_PROMPT,
                user_prompt=prompt,
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=2000
            )
            return response
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            raise

    def _parse_response(self, response: str) -> JobAnalysis:
        """
        Parse the LLM response into a JobAnalysis object.

        Args:
            response: The raw LLM response string.

        Returns:
            JobAnalysis object.

        Raises:
            ValueError: If the response cannot be parsed.
        """
        try:
            # Clean the response - remove markdown code blocks if present
            cleaned_response = response.strip()

            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]

            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]

            cleaned_response = cleaned_response.strip()

            # Parse JSON
            data = json.loads(cleaned_response)

            # Create JobAnalysis object (Pydantic will validate)
            analysis = JobAnalysis(**data)

            return analysis

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.debug(f"Raw response: {response[:500]}")
            raise ValueError(f"Invalid JSON response from LLM: {str(e)}")
        except Exception as e:
            logger.error(f"Error creating JobAnalysis object: {str(e)}")
            raise ValueError(f"Failed to parse LLM response: {str(e)}")

    def _mock_analysis(self, job_description: str) -> str:
        """
        Generate a mock analysis for testing purposes.

        Args:
            job_description: The job description text.

        Returns:
            Mock JSON response.
        """
        # Simple keyword extraction for testing
        text_lower = job_description.lower()

        hard_skills = []
        if "python" in text_lower:
            hard_skills.append("Python")
        if "aws" in text_lower or "amazon web services" in text_lower:
            hard_skills.append("AWS")
        if "docker" in text_lower:
            hard_skills.append("Docker")
        if "kubernetes" in text_lower or "k8s" in text_lower:
            hard_skills.append("Kubernetes")

        soft_skills = []
        if "leadership" in text_lower or "lead" in text_lower:
            soft_skills.append("Leadership")
        if "communication" in text_lower:
            soft_skills.append("Communication")
        if "team" in text_lower:
            soft_skills.append("Teamwork")

        mock_data = {
            "hard_skills": hard_skills if hard_skills else ["General IT Skills"],
            "soft_skills": soft_skills if soft_skills else ["Communication", "Problem-solving"],
            "qualifications": ["Bachelor's degree in Computer Science or related field"],
            "experience_required": "3-5 years",
            "key_responsibilities": [
                "Develop and maintain software applications",
                "Collaborate with cross-functional teams",
                "Participate in code reviews"
            ],
            "keywords": ["software", "development", "technical", "engineering"],
            "culture_keywords": ["collaborative", "innovative"],
            "nice_to_have": ["Master's degree", "Cloud certifications"],
            "action_verbs": ["develop", "implement", "design", "collaborate"],
            "company_name": None,
            "job_title": "Software Engineer",
            "location": "Remote"
        }

        return json.dumps(mock_data)

    def extract_from_file(self, file_path: str) -> JobAnalysis:
        """
        Extract keywords from a job description file.

        Args:
            file_path: Path to the job description file.

        Returns:
            JobAnalysis object.
        """
        from ..tools.file_reader import FileReaderTool

        reader = FileReaderTool()
        job_description = reader.read_file(file_path)

        return self.analyze_job_description(job_description)
