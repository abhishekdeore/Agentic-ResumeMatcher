@echo off
echo ================================================
echo    Agentic Resume Matcher - Web Application
echo ================================================
echo.
echo Starting server...
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python run_app.py

pause
