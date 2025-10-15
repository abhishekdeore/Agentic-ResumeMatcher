# Contributing to Agentic Resume Matcher

Thank you for considering contributing to Agentic Resume Matcher! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Your environment (OS, Python version, etc.)
   - Relevant logs or screenshots

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Potential implementation approach
   - Any alternatives considered

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Write/update tests
5. Update documentation
6. Ensure tests pass: `pytest`
7. Format code: `black src/ tests/`
8. Commit with clear message
9. Push to your fork
10. Create a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/agentic-resume-matcher.git
cd agentic-resume-matcher

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Code Standards

### Python Style

- Follow PEP 8
- Use Black for formatting: `black src/ tests/`
- Use isort for imports: `isort src/ tests/`
- Type hints where appropriate
- Docstrings for all public functions/classes

### Testing

- Write tests for new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Use fixtures for common test data

### Documentation

- Update README.md if needed
- Add docstrings to new functions/classes
- Update relevant documentation in docs/
- Include examples for new features

### Commit Messages

Format:
```
type: Brief description (50 chars max)

Detailed explanation if needed.
Mention any breaking changes.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## Testing Guidelines

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents/test_keyword_extractor.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_tools/test_file_reader.py::test_read_text_file
```

## Documentation Guidelines

- Use clear, concise language
- Provide examples
- Keep README.md updated
- Document breaking changes
- Update CHANGELOG.md

## Project Structure

When adding new features:

```
src/
├── agents/       # AI agents
├── tools/        # Utility tools
├── models/       # Data models
├── config/       # Configuration
└── utils/        # Helper functions

tests/
├── test_agents/  # Agent tests
├── test_tools/   # Tool tests
└── fixtures/     # Test data
```

## What to Contribute

### Good First Issues

- Bug fixes
- Documentation improvements
- Test coverage improvements
- Code cleanup and refactoring

### Advanced Contributions

- New features
- Performance improvements
- New LLM provider support
- Additional file format support
- Enhanced parsing algorithms

### Ideas for Contribution

- Add support for more file formats
- Implement caching for repeated analyses
- Create web interface
- Add resume templates
- Improve matching algorithm
- Add batch processing
- Create cover letter generator
- Add internationalization

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, it will be merged
4. Your contribution will be credited

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in relevant documentation

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
