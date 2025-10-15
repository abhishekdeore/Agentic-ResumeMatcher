"""FastAPI server example for Resume Tailoring System.

This provides a REST API interface for the resume tailoring functionality.

Run with: uvicorn examples.api_example:app --reload
"""

import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import create_resume_tailor_system
from src.models.resume_data import ResumeRequest
from src.config.settings import get_settings
from src.utils.logger import setup_logging

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Resume Matcher API",
    description="AI-powered resume tailoring API",
    version="0.1.0"
)

# Setup templates
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system
settings = get_settings()
setup_logging(log_level=settings.log_level)
system = create_resume_tailor_system(model_provider=settings.model_provider)


# Request/Response Models
class JobAnalysisRequest(BaseModel):
    """Request model for job analysis endpoint."""
    job_description: str


class JobAnalysisResponse(BaseModel):
    """Response model for job analysis."""
    job_title: Optional[str]
    company_name: Optional[str]
    hard_skills: list[str]
    soft_skills: list[str]
    experience_required: str
    keywords: list[str]


class TailorResponse(BaseModel):
    """Response model for resume tailoring."""
    tailored_resume: str
    match_score: Optional[float]
    keywords_matched: list[str]
    suggestions: list[str]
    output_path: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the web interface."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api", response_model=HealthResponse)
async def api_info():
    """API information endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.post("/analyze")
async def analyze_resume_match(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    """
    Analyze how well a resume matches a job description WITHOUT tailoring.
    Returns match score, matched keywords, and missing keywords.

    Args:
        job_description: Job description text
        resume_file: Resume file upload (.txt, .pdf, .docx)

    Returns:
        Analysis with match score and keyword details
    """
    temp_resume_path = None

    try:
        # Save uploaded resume to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as temp_resume:
            content = await resume_file.read()
            temp_resume.write(content)
            temp_resume_path = temp_resume.name

        # Read resume
        from src.tools.file_reader import FileReaderTool
        file_reader = FileReaderTool()
        resume_text = file_reader.read_file(temp_resume_path)

        # Analyze job description
        job_analysis = system.keyword_extractor.analyze_job_description(job_description)

        # Calculate match score
        match_score = system.resume_tailor.calculate_match_score(resume_text, job_analysis)

        # Identify matched and missing keywords
        matched_keywords = system.resume_tailor.identify_matched_keywords(resume_text, job_analysis)

        all_keywords = job_analysis.get_all_keywords()
        missing_keywords = [kw for kw in all_keywords if kw not in matched_keywords]

        # Generate suggestions
        suggestions = []
        if missing_keywords[:10]:
            suggestions.append(f"Consider adding these relevant skills: {', '.join(missing_keywords[:10])}")

        if match_score < 50:
            suggestions.append("Your resume match is below 50%. Consider emphasizing relevant experience.")

        if not any(char.isdigit() for char in resume_text):
            suggestions.append("Add quantifiable metrics to demonstrate your impact.")

        return {
            "match_score": match_score,
            "job_title": job_analysis.job_title,
            "company_name": job_analysis.company_name,
            "matched_keywords": matched_keywords[:20],
            "missing_keywords": missing_keywords[:20],
            "suggestions": suggestions,
            "hard_skills_required": job_analysis.hard_skills,
            "soft_skills_required": job_analysis.soft_skills
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Cleanup temp files
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.unlink(temp_resume_path)


@app.post("/tailor", response_model=TailorResponse)
async def tailor_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    output_format: str = Form("markdown"),
    calculate_score: bool = Form(True)
):
    """
    Tailor a resume to a job description.

    Args:
        job_description: Job description text
        resume_file: Resume file upload (.txt, .pdf, .docx)
        output_format: Output format (markdown, txt, pdf)
        calculate_score: Whether to calculate match score

    Returns:
        Tailored resume and analysis
    """
    temp_resume_path = None
    temp_output_path = None

    try:
        # Save uploaded resume to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as temp_resume:
            content = await resume_file.read()
            temp_resume.write(content)
            temp_resume_path = temp_resume.name

        # Create request
        request = ResumeRequest(
            job_description=job_description,
            resume_file_path=temp_resume_path,
            output_format=output_format,
            calculate_match_score=calculate_score
        )

        # Process
        result = system.process_resume(request)

        # Prepare response
        response = {
            "tailored_resume": result.tailored_resume,
            "match_score": result.match_score,
            "keywords_matched": result.keywords_matched[:20],  # Limit size
            "suggestions": result.suggestions,
            "output_path": result.output_path or ""
        }

        return response

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tailoring failed: {str(e)}")
    finally:
        # Cleanup temp files
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.unlink(temp_resume_path)


@app.post("/tailor/download")
async def tailor_and_download(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...),
    output_format: str = Form("pdf")
):
    """
    Tailor resume and return as downloadable file.

    Args:
        job_description: Job description text
        resume_file: Resume file upload
        output_format: Output format for download

    Returns:
        Tailored resume as downloadable file
    """
    temp_resume_path = None

    try:
        # Save uploaded resume
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume_file.filename).suffix) as temp_resume:
            content = await resume_file.read()
            temp_resume.write(content)
            temp_resume_path = temp_resume.name

        # Process
        result = system.tailor_resume(
            job_description=job_description,
            resume_path=temp_resume_path,
            output_format=output_format
        )

        # Return file
        if result.output_path and os.path.exists(result.output_path):
            return FileResponse(
                result.output_path,
                media_type="application/octet-stream",
                filename=f"tailored_resume.{output_format}"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to generate output file")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tailoring failed: {str(e)}")
    finally:
        if temp_resume_path and os.path.exists(temp_resume_path):
            os.unlink(temp_resume_path)


@app.get("/config")
async def get_config():
    """Get current system configuration (non-sensitive data only)."""
    config = get_settings()

    return {
        "model_provider": config.model_provider,
        "model_id": config.model_id,
        "output_directory": config.output_directory,
        "log_level": config.log_level,
        "supported_formats": config.supported_formats
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


if __name__ == "__main__":
    import uvicorn

    print("Starting Agentic Resume Matcher API Server...")
    print("API docs available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")

    uvicorn.run(
        "api_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
