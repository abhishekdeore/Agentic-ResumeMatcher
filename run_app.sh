#!/bin/bash

echo "================================================"
echo "   Agentic Resume Matcher - Web Application"
echo "================================================"
echo ""
echo "Starting server..."
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python run_app.py
