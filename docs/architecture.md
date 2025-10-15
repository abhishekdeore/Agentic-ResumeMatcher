# System Architecture

Detailed architecture documentation for the Agentic Resume Matcher system.

## Overview

The Agentic Resume Matcher is built on a multi-agent architecture where specialized AI agents collaborate to analyze job descriptions and optimize resumes. The system follows clean architecture principles with clear separation of concerns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                                                               │
│  ┌─────────────┐                    ┌──────────────────┐    │
│  │  CLI (Click)│                    │  Python API      │    │
│  └──────┬──────┘                    └────────┬─────────┘    │
│         │                                     │               │
│         └─────────────────┬───────────────────┘               │
│                           │                                   │
└───────────────────────────┼───────────────────────────────────┘
                            │
┌───────────────────────────┼───────────────────────────────────┐
│               Application Layer (main.py)                     │
│                           │                                   │
│       ┌───────────────────▼─────────────────────┐            │
│       │  ResumeTailoringSystem (Orchestrator)   │            │
│       └───────────┬────────────────┬─────────────┘            │
│                   │                │                          │
└───────────────────┼────────────────┼──────────────────────────┘
                    │                │
┌───────────────────┼────────────────┼──────────────────────────┐
│                   │   Agent Layer  │                          │
│                   │                │                          │
│       ┌───────────▼──────┐  ┌─────▼──────────────┐           │
│       │ KeywordExtractor │  │  ResumeTailor      │           │
│       │     Agent        │  │     Agent          │           │
│       └───────┬──────────┘  └─────┬──────────────┘           │
│               │                    │                          │
└───────────────┼────────────────────┼──────────────────────────┘
                │                    │
┌───────────────┼────────────────────┼──────────────────────────┐
│               │    Tools Layer     │                          │
│               │                    │                          │
│     ┌─────────▼─────┐    ┌────────▼────────┐                 │
│     │ FileReaderTool│    │ FileWriterTool  │                 │
│     └────────────────┘    └─────────────────┘                 │
│                                                                │
│     ┌─────────────────────────────────────┐                   │
│     │      ResumeParserTool               │                   │
│     └─────────────────────────────────────┘                   │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    Infrastructure Layer                        │
│                                                                │
│  ┌──────────┐  ┌────────┐  ┌─────────┐  ┌────────────────┐   │
│  │  Config  │  │ Logger │  │Validator│  │  LLM Provider  │   │
│  │ Settings │  │        │  │         │  │   (Bedrock)    │   │
│  └──────────┘  └────────┘  └─────────┘  └────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### CLI (src/cli.py)
- Built with Click framework
- Provides command-line interface
- Commands: tailor, analyze, parse, config, version
- Handles user input validation
- Displays results with Rich library

#### Python API (src/main.py)
- Programmatic interface for integration
- Factory functions for easy initialization
- Returns structured result objects

### 2. Application Layer

#### ResumeTailoringSystem
**Responsibilities:**
- Orchestrates workflow between agents
- Manages state and progress
- Coordinates file I/O
- Generates final results

**Key Methods:**
- `process_resume()` - Main workflow orchestration
- `tailor_resume()` - Simplified interface
- `display_results()` - User-friendly output

**Workflow:**
1. Load job description
2. Analyze with KeywordExtractorAgent
3. Load original resume
4. Tailor with ResumeTailorAgent
5. Calculate match score
6. Generate output files
7. Return structured results

### 3. Agent Layer

#### KeywordExtractorAgent (src/agents/keyword_extractor.py)

**Purpose:** Analyze job descriptions and extract structured information

**System Prompt Strategy:**
- Acts as expert recruiter with 15+ years experience
- Extracts both explicit and implicit requirements
- Provides context for ambiguous terms
- Returns structured JSON output

**Input:** Job description text

**Output:** JobAnalysis object with:
- Hard skills (technical skills)
- Soft skills (interpersonal skills)
- Qualifications (degrees, certifications)
- Experience requirements
- Key responsibilities
- Industry keywords
- Company culture indicators
- Nice-to-have skills
- Action verbs

**Processing Flow:**
```
Job Description Text
        ↓
    Validate Input (length, format)
        ↓
    Build Prompt (system + user)
        ↓
    Call LLM API
        ↓
    Parse JSON Response
        ↓
    Validate with Pydantic
        ↓
    Return JobAnalysis
```

#### ResumeTailorAgent (src/agents/resume_tailor.py)

**Purpose:** Optimize resumes to match job requirements while maintaining authenticity

**Core Principles:**
1. **Never fabricate** - Only reframe existing content
2. **Natural keyword integration** - No keyword stuffing
3. **Maintain voice** - Keep candidate's authentic style
4. **ATS optimization** - Clear formatting, relevant keywords
5. **Quantify when possible** - Highlight metrics and achievements

**System Prompt Strategy:**
- Acts as professional resume writer and career coach
- 15+ years of ATS optimization expertise
- Strict rules against fabrication
- Focus on strategic storytelling with facts

**Input:**
- Original resume text
- JobAnalysis object
- Optional: full job description for context

**Output:** Tailored resume in Markdown format

**Processing Flow:**
```
Original Resume + Job Analysis
        ↓
    Build Comprehensive Prompt
        ↓
    Call LLM API
        ↓
    Receive Tailored Resume
        ↓
    Calculate Match Score
        ↓
    Identify Matched Keywords
        ↓
    Generate Suggestions
        ↓
    Return Tailored Resume
```

### 4. Tools Layer

#### FileReaderTool (src/tools/file_reader.py)

**Capabilities:**
- Read .txt, .pdf, .docx files
- Handle encoding issues with fallback
- Extract text from encrypted PDFs
- Parse DOCX tables and paragraphs
- Robust error handling

**Methods:**
- `read_file()` - Main reading method
- `validate_file()` - Check file validity
- `get_file_info()` - File metadata

#### FileWriterTool (src/tools/file_writer.py)

**Capabilities:**
- Write Markdown, plain text, PDF
- Professional PDF formatting
- Auto-generate timestamped filenames
- Add metadata headers
- Create comparison documents

**Methods:**
- `write_file()` - Main writing method
- `write_comparison()` - Side-by-side comparison

#### ResumeParserTool (src/tools/parser.py)

**Capabilities:**
- Identify resume sections intelligently
- Extract bullet points
- Parse contact information
- Normalize section headers
- Handle various resume formats

**Parsing Strategy:**
- Pattern matching for common sections
- Heuristic-based header detection
- Regex for contact info extraction
- Bullet point identification

### 5. Data Models Layer

#### Pydantic Models (src/models/)

**JobAnalysis:**
- Structured job description data
- Validation of required fields
- Helper methods for keyword aggregation

**ResumeRequest:**
- Input validation
- Field validators for paths and formats
- Configuration for resume tailoring

**ResumeTailorResult:**
- Complete result object
- Metrics and metadata
- Helper methods for display

**ParsedResume:**
- Structured resume representation
- Section-by-section breakdown
- Contact information extraction

### 6. Infrastructure Layer

#### Configuration (src/config/settings.py)

**Pydantic Settings:**
- Environment variable loading
- .env file support
- Type validation
- Default values

**Settings Categories:**
- Model configuration
- AWS credentials
- Application settings
- Performance options

#### Logging (src/utils/logger.py)

**Loguru-based Logging:**
- Console output with colors
- File logging with rotation
- Context-aware messages
- Performance monitoring

**Log Levels:**
- DEBUG: Detailed diagnostic information
- INFO: General operational messages
- WARNING: Warning messages
- ERROR: Error messages

#### Validators (src/utils/validators.py)

**Input Validation:**
- File path validation
- Format validation
- Size checks
- Extension verification
- Job description validation

## Data Flow

### Complete Workflow Data Flow

```
1. User Input
   ├─ Job Description (file or text)
   └─ Resume File (pdf/docx/txt)
           ↓
2. Input Validation
   ├─ File existence check
   ├─ Format verification
   └─ Size validation
           ↓
3. Job Analysis
   ├─ FileReaderTool reads job description
   ├─ KeywordExtractorAgent analyzes
   ├─ LLM processes with system prompt
   └─ Returns JobAnalysis object
           ↓
4. Resume Loading
   ├─ FileReaderTool reads resume
   ├─ ResumeParserTool parses structure
   └─ Extract text content
           ↓
5. Resume Tailoring
   ├─ ResumeTailorAgent receives:
   │  ├─ Original resume
   │  ├─ JobAnalysis
   │  └─ Context
   ├─ LLM generates tailored version
   └─ Returns optimized resume
           ↓
6. Analysis & Scoring
   ├─ Calculate match score
   ├─ Identify matched keywords
   └─ Generate suggestions
           ↓
7. Output Generation
   ├─ FileWriterTool writes tailored resume
   ├─ Optional: Generate comparison
   └─ Create result object
           ↓
8. Results Display
   ├─ Format with Rich
   ├─ Show metrics
   └─ Display suggestions
```

## Design Patterns

### 1. Factory Pattern
```python
def create_resume_tailor_system(model_provider, ...):
    # Creates configured system instance
```

### 2. Strategy Pattern
Different file readers for different formats:
- `_read_text()` for .txt
- `_read_pdf()` for .pdf
- `_read_docx()` for .docx

### 3. Template Method Pattern
Base workflow in `ResumeTailoringSystem.process_resume()`

### 4. Singleton Pattern
Global settings instance via `get_settings()`

### 5. Builder Pattern
`ResumeRequest` and `JobAnalysis` construction

## Extension Points

### Adding New File Formats

```python
# In FileReaderTool
def _read_new_format(self, path: Path) -> str:
    # Implement new format reading
    pass
```

### Adding New LLM Providers

```python
# In main.py
if model_provider == "new_provider":
    client = NewProviderClient(api_key=api_key)
```

### Custom Agents

```python
class CustomAgent:
    def __init__(self, model_client):
        self.model_client = model_client

    def process(self, input_data):
        # Custom processing logic
        pass
```

### Additional Output Formats

```python
# In FileWriterTool
def _write_new_format(self, content, path):
    # Implement new format writing
    pass
```

## Security Considerations

1. **Input Validation:** All user inputs validated before processing
2. **File Size Limits:** Prevent resource exhaustion
3. **Path Traversal:** Sanitize file paths
4. **API Key Protection:** Environment variables only
5. **Logging:** Sensitive data not logged

## Performance Considerations

1. **Caching:** Optional caching for repeated job analyses
2. **Async Operations:** Potential for concurrent processing
3. **Token Optimization:** Careful prompt engineering
4. **Rate Limiting:** Respect API limits

## Error Handling Strategy

1. **Validation Errors:** Caught early with clear messages
2. **File Errors:** Specific error types (not found, corrupt, etc.)
3. **API Errors:** Retry logic and fallbacks
4. **Parse Errors:** Graceful degradation

## Testing Strategy

1. **Unit Tests:** Individual components
2. **Integration Tests:** End-to-end workflows
3. **Fixtures:** Sample data for testing
4. **Mocking:** LLM calls mocked for testing

## Future Enhancements

1. **Batch Processing:** Multiple resumes/jobs at once
2. **Cover Letter Generation:** Additional agent
3. **Interview Prep:** Questions based on job
4. **Web Interface:** Browser-based UI
5. **Resume Templates:** Multiple styling options
6. **ML Match Scoring:** Enhanced scoring algorithm
7. **Database Storage:** Track history and versions
8. **API Server:** RESTful API with FastAPI

## Monitoring and Observability

1. **Logging:** Comprehensive logs at all levels
2. **Metrics:** Track success rates, latency
3. **Error Tracking:** Detailed error information
4. **Usage Analytics:** API call patterns

## Deployment Architecture

### Local Development
```
Developer Machine
├─ Python 3.9+
├─ Virtual Environment
├─ .env configuration
└─ Direct AWS Bedrock access
```

### Production (Future)
```
Cloud Infrastructure
├─ Docker Container
├─ Load Balancer
├─ API Gateway
├─ Secrets Manager
└─ CloudWatch Logging
```

## Summary

The Agentic Resume Matcher demonstrates:
- Clean architecture with separation of concerns
- Modular design for easy extension
- Robust error handling
- Production-ready code practices
- Clear data flow
- Comprehensive testing strategy
- Security-first approach

The multi-agent architecture allows each component to focus on its specialty, resulting in high-quality, maintainable, and extensible code.
