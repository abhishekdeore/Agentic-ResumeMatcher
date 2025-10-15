# Usage Guide

Comprehensive guide for using the Agentic Resume Matcher system.

## Table of Contents
- [Quick Start](#quick-start)
- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)

## Quick Start

### Basic Resume Tailoring

```bash
python -m src.cli tailor \
  --job-description job.txt \
  --resume my_resume.pdf \
  --format markdown
```

This will:
1. Analyze the job description
2. Extract keywords and requirements
3. Tailor your resume
4. Save the result to `output/tailored_resume_TIMESTAMP.md`

## Command Line Interface

### 1. Tailor Command

Main command for tailoring resumes to job descriptions.

```bash
python -m src.cli tailor [OPTIONS]
```

**Required Options:**
- `-j, --job-description TEXT` - Job description (file path or text)
- `-r, --resume TEXT` - Path to your resume file

**Optional Options:**
- `-o, --output TEXT` - Custom output file path
- `-f, --format [markdown|txt|pdf]` - Output format (default: markdown)
- `--comparison` - Generate side-by-side comparison
- `--model-provider [bedrock|openai|anthropic]` - LLM provider
- `--model-id TEXT` - Specific model ID

**Examples:**

```bash
# Basic usage with default settings
python -m src.cli tailor -j job.txt -r resume.pdf

# Custom output path and PDF format
python -m src.cli tailor \
  -j job.txt \
  -r resume.docx \
  -o my_tailored_resume.pdf \
  -f pdf

# With comparison and specific model
python -m src.cli tailor \
  -j job.txt \
  -r resume.pdf \
  --comparison \
  --model-provider bedrock \
  --model-id us.anthropic.claude-sonnet-4-20250514-v1:0

# Using job description as text (for short descriptions)
python -m src.cli tailor \
  -j "Senior Python Developer. 5+ years experience. AWS, Docker, FastAPI required." \
  -r resume.pdf
```

### 2. Analyze Command

Analyze a job description without tailoring a resume.

```bash
python -m src.cli analyze -j job_description.txt
```

**Output:**
- Job title and company (if found)
- Required hard skills
- Required soft skills
- Experience level
- Key responsibilities
- Important keywords

**Example:**

```bash
python -m src.cli analyze -j "Senior Data Scientist position requiring Python, ML, and 5 years experience..."
```

### 3. Parse Command

Parse and display resume structure.

```bash
python -m src.cli parse -r resume.pdf --format markdown
```

**Output:**
- Detected sections
- Contact information
- Bullet points count
- Content preview

**Example:**

```bash
python -m src.cli parse -r my_resume.docx
```

### 4. Config Command

Display current configuration.

```bash
python -m src.cli config
```

Shows:
- Model settings
- AWS configuration
- Output directory
- Log level

### 5. Version Command

Display version information.

```bash
python -m src.cli version
```

## Python API

### Basic Usage

```python
from src.main import create_resume_tailor_system

# Initialize system
system = create_resume_tailor_system(model_provider="bedrock")

# Tailor resume
result = system.tailor_resume(
    job_description="path/to/job.txt",
    resume_path="path/to/resume.pdf",
    output_format="markdown"
)

# Access results
print(f"Match score: {result.match_score}%")
print(f"Matched keywords: {result.keywords_matched}")
print(f"Output: {result.output_path}")
```

### Using Request Objects

```python
from src.models.resume_data import ResumeRequest

# Create detailed request
request = ResumeRequest(
    job_description="path/to/job.txt",
    resume_file_path="path/to/resume.pdf",
    output_format="pdf",
    output_path="./output/my_resume.pdf",
    show_comparison=True,
    calculate_match_score=True
)

# Process
result = system.process_resume(request)

# Display results
system.display_results(result)
```

### Analyzing Jobs Only

```python
from src.agents.keyword_extractor import KeywordExtractorAgent

extractor = KeywordExtractorAgent()

# Analyze job description
analysis = extractor.analyze_job_description(job_text)

# Access extracted data
print(f"Hard skills: {analysis.hard_skills}")
print(f"Soft skills: {analysis.soft_skills}")
print(f"Experience: {analysis.experience_required}")
```

### Working with Individual Agents

```python
from src.agents.keyword_extractor import KeywordExtractorAgent
from src.agents.resume_tailor import ResumeTailorAgent

# Step 1: Extract keywords
extractor = KeywordExtractorAgent()
job_analysis = extractor.analyze_job_description(job_text)

# Step 2: Tailor resume
tailor = ResumeTailorAgent()
tailored = tailor.tailor_resume(
    original_resume=resume_text,
    job_analysis=job_analysis
)

# Step 3: Calculate match score
score = tailor.calculate_match_score(tailored, job_analysis)
print(f"Match: {score}%")
```

### File Operations

```python
from src.tools.file_reader import FileReaderTool
from src.tools.file_writer import FileWriterTool

# Read files
reader = FileReaderTool()
resume_text = reader.read_file("resume.pdf")
job_text = reader.read_file("job.docx")

# Write files
writer = FileWriterTool(output_directory="./output")
output_path = writer.write_file(
    content=tailored_resume,
    output_format="pdf",
    job_title="Senior Engineer"
)
```

## Advanced Usage

### Batch Processing

Process multiple resumes or job descriptions:

```python
import glob
from src.main import create_resume_tailor_system

system = create_resume_tailor_system()

# Process multiple job descriptions with same resume
resume_path = "my_resume.pdf"
job_files = glob.glob("jobs/*.txt")

for job_file in job_files:
    result = system.tailor_resume(
        job_description=job_file,
        resume_path=resume_path,
        output_format="pdf"
    )
    print(f"Processed: {job_file} -> {result.output_path}")
```

### Custom Configuration

```python
from src.config.settings import Settings
from src.main import ResumeTailoringSystem

# Create custom configuration
config = Settings(
    model_provider="bedrock",
    model_id="custom-model-id",
    temperature=0.5,
    max_tokens=3000,
    output_directory="./custom_output"
)

# Create system with custom config
system = ResumeTailoringSystem(config=config)
```

### Error Handling

```python
from src.main import create_resume_tailor_system

system = create_resume_tailor_system()

try:
    result = system.tailor_resume(
        job_description="job.txt",
        resume_path="resume.pdf"
    )
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Logging Configuration

```python
from src.utils.logger import setup_logging

# Configure detailed logging
setup_logging(
    log_level="DEBUG",
    log_file="./logs/app.log"
)

# Now run your operations with detailed logs
```

## Best Practices

### 1. Prepare Quality Inputs

**Good Job Description:**
- Complete posting with all details
- Clear requirements section
- Specific skills and qualifications
- Company information

**Good Resume:**
- Well-structured with clear sections
- Quantifiable achievements
- Specific skills listed
- Recent and relevant experience

### 2. Review Outputs

Always review the tailored resume:
- Check for accuracy
- Ensure it sounds natural
- Verify all statements are truthful
- Customize further if needed

### 3. Iterate and Improve

- Generate multiple versions
- Try different output formats
- Use suggestions to improve base resume
- Keep track of what works

### 4. File Organization

```bash
project/
├── resumes/
│   ├── base_resume.pdf
│   └── tailored/
│       ├── company1_role.pdf
│       └── company2_role.pdf
└── jobs/
    ├── company1_job.txt
    └── company2_job.txt
```

### 5. Version Control

Keep track of resume versions:
```bash
# Name files descriptively
tailored_resume_CompanyName_Role_2024-01-15.pdf
```

### 6. Privacy and Security

- Don't include sensitive personal information
- Remove references before sharing examples
- Be cautious with API keys
- Review logs before sharing

## Common Workflows

### Workflow 1: Quick Application

```bash
# 1. Analyze the job
python -m src.cli analyze -j job.txt

# 2. Tailor your resume
python -m src.cli tailor -j job.txt -r resume.pdf -f pdf

# 3. Review output file
# 4. Submit application
```

### Workflow 2: Multiple Positions

```bash
# Tailor for multiple similar positions
for job in jobs/*.txt; do
    python -m src.cli tailor \
        -j "$job" \
        -r base_resume.pdf \
        -o "output/$(basename $job .txt)_resume.pdf" \
        -f pdf
done
```

### Workflow 3: Iterative Improvement

```python
# Python script for iterative improvement
system = create_resume_tailor_system()

result = system.tailor_resume(
    job_description="job.txt",
    resume_path="resume.pdf",
    show_comparison=True
)

# Review suggestions
for suggestion in result.suggestions:
    print(f"- {suggestion}")

# Update base resume based on suggestions
# Re-run tailoring
```

## Tips for Best Results

1. **Use Complete Job Descriptions**: More details = better tailoring
2. **Start with Good Base Resume**: Quality in = Quality out
3. **Check Match Scores**: Aim for 70%+ match
4. **Use Comparison Feature**: Learn what changes were made
5. **Incorporate Suggestions**: Improve your base resume over time
6. **Test Different Formats**: PDF for applications, Markdown for edits
7. **Keep It Truthful**: System won't fabricate - don't manually add false info
8. **Update Regularly**: Tailor for each application

## Troubleshooting

### Low Match Score

- Ensure your experience is relevant to the role
- Check if key skills are present in original resume
- Consider if the position is a good fit

### Poor Output Quality

- Provide more detailed job description
- Improve base resume structure
- Check input file quality (clear text, not scanned images)

### Slow Performance

- Reduce max_tokens in configuration
- Use faster model
- Check internet connection
- Verify API rate limits

## Next Steps

- Read [Architecture Documentation](architecture.md)
- Explore [Example Scripts](../examples/)
- Review [API Documentation](#) (if available)
- Join community discussions

## Support

For issues or questions:
- Check documentation
- Review examples
- Create GitHub issue
- Contact support
