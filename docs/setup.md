# Setup Guide

Complete guide for setting up the Agentic Resume Matcher system.

## Prerequisites

- Python 3.9 or higher
- pip or Poetry package manager
- AWS account (for Bedrock access) or API keys for alternative providers
- Git (for cloning the repository)

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd agentic-resume-matcher
```

### 2. Create Virtual Environment

**Using venv (recommended):**
```bash
python -m venv venv

# Activate on Linux/Mac:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n resume-matcher python=3.9
conda activate resume-matcher
```

### 3. Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using Poetry:**
```bash
poetry install
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Model Configuration
MODEL_PROVIDER=bedrock
MODEL_ID=us.anthropic.claude-sonnet-4-20250514-v1:0
AWS_REGION=us-west-2
TEMPERATURE=0.7
MAX_TOKENS=4000

# AWS Credentials (for Bedrock)
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here

# Application Settings
OUTPUT_DIRECTORY=./output
LOG_LEVEL=INFO
```

## AWS Bedrock Setup

### 1. Create AWS Account
If you don't have an AWS account:
1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process

### 2. Create IAM User for Bedrock

1. Log in to AWS Console
2. Navigate to IAM (Identity and Access Management)
3. Click "Users" → "Add users"
4. Create a user with programmatic access
5. Attach the `AmazonBedrockFullAccess` policy
6. Save the Access Key ID and Secret Access Key

### 3. Request Model Access

1. Go to AWS Bedrock console
2. Click "Model access" in the left sidebar
3. Click "Request model access"
4. Select Anthropic Claude models:
   - Claude 3 Sonnet
   - Claude 3.5 Sonnet (recommended)
5. Submit request
6. Access is usually granted immediately

### 4. Configure AWS Credentials

**Option 1: Environment Variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=us-west-2
```

**Option 2: AWS CLI Configuration**
```bash
aws configure
# Enter your credentials when prompted
```

**Option 3: .env File**
Add credentials to `.env` file (recommended for development)

## Alternative LLM Providers

### OpenAI Setup

```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
MODEL_ID=gpt-4
```

### Anthropic Direct Setup

```env
MODEL_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key
MODEL_ID=claude-3-sonnet-20240229
```

## Verify Installation

### 1. Check Python Version
```bash
python --version
# Should be 3.9 or higher
```

### 2. Test Imports
```bash
python -c "import src; print('Imports successful')"
```

### 3. Run Tests
```bash
pytest tests/
```

### 4. Check Configuration
```bash
python -m src.cli config
```

This should display your current configuration without errors.

## Project Structure Setup

The following directories will be created automatically when needed:
- `output/` - For generated resumes
- `logs/` - For application logs (if enabled)

You can create them manually:
```bash
mkdir output logs
```

## Development Setup (Optional)

For contributors and developers:

### Install Development Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Using Poetry
poetry install --with dev
```

### Install Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

### Configure IDE

**VS Code:**
Create `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

**PyCharm:**
1. Open Settings → Tools → Python Integrated Tools
2. Set Default test runner to pytest
3. Enable black formatting

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall packages
pip install -r requirements.txt
```

### Issue: AWS Credentials Error

**Solution:**
```bash
# Verify credentials
aws sts get-caller-identity

# Or check .env file
cat .env | grep AWS
```

### Issue: Bedrock Access Denied

**Solution:**
1. Check that you've requested model access in Bedrock console
2. Verify IAM user has correct permissions
3. Ensure region is correct (us-west-2 or us-east-1)

### Issue: PDF Reading Fails

**Solution:**
```bash
# On Ubuntu/Debian
sudo apt-get install python3-dev

# On macOS
brew install libxml2 libxslt

# Reinstall PyPDF2
pip install --upgrade PyPDF2
```

### Issue: Port Issues

**Solution:**
If running the FastAPI server and port 8000 is busy:
```bash
# Use a different port
uvicorn src.api:app --port 8080
```

## Next Steps

After successful setup:

1. Read the [Usage Guide](usage.md) for examples
2. Review [Architecture Documentation](architecture.md)
3. Try the example in `examples/cli_example.py`
4. Start tailoring your resume!

## Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
pytest
```

## Uninstallation

To remove the project:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf agentic-resume-matcher
```

## Support

If you encounter issues:
1. Check this setup guide thoroughly
2. Review the troubleshooting section
3. Check existing GitHub issues
4. Create a new issue with details about your setup and error

## Security Notes

- Never commit `.env` file to version control
- Rotate AWS credentials regularly
- Use IAM roles with minimal required permissions
- Store API keys securely
- Don't share credentials in screenshots or logs
