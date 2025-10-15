"""Simple script to run the web application with frontend."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🎯 Agentic Resume Matcher - Web Application")
    print("=" * 60)
    print()
    print("Starting server...")
    print("📱 Web Interface: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("📖 Alternative API Docs: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    uvicorn.run(
        "examples.api_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
