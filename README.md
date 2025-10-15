# 🎯 Agentic Resume Matcher

> **AI-Powered Resume Analysis & Tailoring System** using Multi-Agent Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

A production-ready application that uses multi-agent AI architecture to intelligently analyze and tailor resumes to specific job descriptions. Get instant match scores, keyword analysis, and AI-optimized resumes that pass ATS (Applicant Tracking Systems).

![Demo](https://via.placeholder.com/800x400?text=Agentic+Resume+Matcher+Demo)

## ✨ Key Features

### 🔍 **Two-Stage Workflow**
- **Stage 1 - Analysis**: Get match score, matched/missing keywords, and recommendations WITHOUT modifying your resume
- **Stage 2 - Improvement**: AI agents tailor your resume based on analysis insights

### 🤖 **Real-Time Agent Visualization**
- Watch AI agents work in real-time with animated progress indicators
- See exactly what each agent is doing (analyzing, optimizing, incorporating keywords)
- Never wonder what's happening - full transparency

### 📊 **Detailed Analysis**
- **Match Score**: Color-coded percentage (Red <50%, Yellow 50-70%, Green >70%)
- **Matched Keywords**: See what skills you already have (green badges)
- **Missing Keywords**: Discover what you're missing (yellow badges)
- **AI Recommendations**: Get actionable suggestions for improvement

### ✨ **Smart Resume Tailoring**
- **Keyword Highlighting**: All incorporated keywords highlighted in green
- **Before/After Comparison**: See score improvement side-by-side
- **ATS Optimization**: Ensures compatibility with Applicant Tracking Systems
- **Authentic Content**: Never fabricates - only optimizes existing content

### 🎨 **Beautiful Web Interface**
- Modern, responsive design
- Smooth animations and transitions
- Real-time progress updates
- Mobile-friendly

### 🛠️ **Multiple Interfaces**
- **Web UI** (Recommended): Beautiful browser interface
- **CLI**: Command-line for power users
- **Python API**: Integrate into your applications
- **REST API**: FastAPI server with OpenAPI docs

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenAI API key **OR** AWS account with Bedrock access

### Installation (3 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/abhishekdeore/Agentic-ResumeMatcher.git
cd Agentic-ResumeMatcher

# 2. Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure your API keys
cp .env.example .env
# Edit .env and add your credentials (see Configuration section)
```

### Configuration

Create a `.env` file with your API credentials:

**Option A: Using OpenAI (Recommended for beginners)**
```env
MODEL_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL_ID=gpt-4o-mini

TEMPERATURE=0.7
MAX_TOKENS=4000
OUTPUT_DIRECTORY=./output
LOG_LEVEL=INFO
```

**Option B: Using AWS Bedrock**
```env
MODEL_PROVIDER=bedrock
MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-west-2

TEMPERATURE=0.7
MAX_TOKENS=4000
OUTPUT_DIRECTORY=./output
LOG_LEVEL=INFO
```

### Running the Application

**Web Interface (Recommended):**
```bash
python run_app.py
```

Then open your browser to: **http://localhost:8000**

**Command Line:**
```bash
python -m src.cli tailor \
  --job-description job.txt \
  --resume resume.pdf \
  --format markdown
```

## 📱 Web Interface Usage

1. **Open** http://localhost:8000 in your browser
2. **Paste** the job description in the text area
3. **Upload** your resume (PDF, DOCX, or TXT)
4. **Click** "🔍 Analyze Resume Match"
5. **Review** match score, matched/missing keywords, and suggestions
6. **Click** "✨ Improve My Resume with AI" (optional)
7. **Watch** agents work in real-time
8. **Review** before/after comparison with keyword highlighting
9. **Download** your tailored resume

## 🏗️ Architecture

### Multi-Agent System

**KeywordExtractorAgent**
- Analyzes job descriptions using AI
- Extracts required skills (hard and soft)
- Identifies qualifications and experience requirements
- Extracts key responsibilities and industry keywords
- Outputs structured data

**ResumeTailorAgent**
- Analyzes original resume content
- Matches experience with job requirements
- Rewrites content to emphasize relevant skills
- Incorporates keywords naturally (no stuffing)
- **Never fabricates** - only optimizes existing content
- Generates ATS-optimized output

### Technology Stack

- **Backend**: Python 3.9+, FastAPI, Pydantic
- **AI**: OpenAI GPT-4o-mini / AWS Bedrock Claude 3.5 Sonnet
- **Frontend**: Vanilla JavaScript, Modern CSS
- **File Processing**: PyPDF2, python-docx, ReportLab
- **CLI**: Click, Rich
- **Testing**: Pytest

## 📂 Project Structure

```
Agentic-ResumeMatcher/
├── src/
│   ├── agents/                 # AI agents
│   │   ├── keyword_extractor.py
│   │   └── resume_tailor.py
│   ├── tools/                  # Utility tools
│   │   ├── file_reader.py
│   │   ├── file_writer.py
│   │   └── parser.py
│   ├── models/                 # Data models
│   │   ├── job_analysis.py
│   │   └── resume_data.py
│   ├── config/                 # Configuration
│   │   └── settings.py
│   ├── llm/                    # LLM clients
│   │   ├── bedrock_client.py
│   │   └── openai_client.py
│   ├── utils/                  # Utilities
│   ├── main.py                 # Core logic
│   └── cli.py                  # CLI interface
├── templates/
│   └── index.html              # Web frontend
├── examples/
│   ├── cli_example.py
│   └── api_example.py          # FastAPI server
├── tests/                      # Test suite
├── output/                     # Generated resumes
├── .env.example                # Example configuration
├── requirements.txt
├── run_app.py                  # Web app launcher
└── README.md
```

## 🎯 CLI Commands

### Tailor Resume
```bash
python -m src.cli tailor \
  --job-description job.txt \
  --resume resume.pdf \
  --format markdown \
  --comparison
```

### Analyze Job Description
```bash
python -m src.cli analyze --job-description job.txt
```

### Parse Resume
```bash
python -m src.cli parse --resume resume.pdf
```

### View Configuration
```bash
python -m src.cli config
```

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PROVIDER` | LLM provider (openai/bedrock) | bedrock |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `OPENAI_MODEL_ID` | OpenAI model | gpt-4o-mini |
| `AWS_ACCESS_KEY_ID` | AWS access key | - |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | - |
| `AWS_REGION` | AWS region | us-west-2 |
| `MODEL_ID` | Bedrock model ID | claude-3-5-sonnet |
| `TEMPERATURE` | Model temperature | 0.7 |
| `MAX_TOKENS` | Max tokens per request | 4000 |
| `OUTPUT_DIRECTORY` | Output location | ./output |
| `LOG_LEVEL` | Logging level | INFO |

## 🧪 Development

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test
pytest tests/test_agents/test_keyword_extractor.py
```

### Code Quality
```bash
# Format
black src/ tests/

# Lint
flake8 src/

# Type check
mypy src/
```

## 🐛 Troubleshooting

### OpenAI "Insufficient Quota" Error
- Add billing information at https://platform.openai.com/account/billing
- Add at least $5 in credits
- Or switch to AWS Bedrock in `.env`

### AWS "Credentials Not Found"
- Verify `.env` file exists with correct credentials
- Run `aws configure` to set up AWS CLI
- Check IAM permissions for Bedrock access

### "Model Access Denied" (AWS Bedrock)
1. Go to AWS Bedrock console
2. Navigate to "Model access"
3. Request access to Anthropic Claude models
4. Wait for approval (usually instant)

### Port 8000 Already in Use
```bash
# Use different port
uvicorn examples.api_example:app --port 8080
```

## 💡 Tips for Best Results

1. **Use Complete Job Descriptions**: More details = better analysis
2. **Start with a Good Resume**: AI optimizes, doesn't create from scratch
3. **Review Before Submitting**: Always review AI output
4. **Iterate**: Use suggestions to improve your base resume
5. **Test Different Formats**: Try markdown, text, and PDF

## 🔒 Privacy & Security

- **No Data Storage**: Resumes are processed in memory, not stored
- **No External Sharing**: Data only sent to chosen LLM provider
- **Environment Variables**: API keys stored securely in `.env`
- **Input Validation**: All inputs sanitized and validated
- **.gitignore**: Ensures sensitive files never committed

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with:
- [OpenAI GPT-4](https://openai.com/) / [Anthropic Claude](https://anthropic.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Rich](https://rich.readthedocs.io/)
- [Click](https://click.palletsprojects.com/)

## 📞 Support

- **Documentation**: See `docs/` directory
- **Issues**: [GitHub Issues](https://github.com/abhishekdeore/Agentic-ResumeMatcher/issues)
- **Examples**: See `examples/` directory

---

**Made with ❤️ for job seekers everywhere**

*Help land your dream job with AI-powered resume optimization!* 🚀

