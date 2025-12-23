# Contributing to Dutch AI Voice Assistant

We appreciate your interest in contributing to the Dutch AI Voice Assistant project! This document provides guidelines and instructions for contributing.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with a clear title
3. Include:
   - Description of the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Your environment (Python version, OS, etc.)

### Suggesting Enhancements

1. Use the issue tracker with clear title and description
2. Explain the use case and expected behavior
3. Include code examples if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Follow code style**:
   - Use Python PEP 8 guidelines
   - Include docstrings for functions
   - Add type hints where applicable
4. **Write tests** for new functionality
5. **Test locally**: `pytest tests/ -v`
6. **Commit with clear messages**: `git commit -m 'Add feature: description'`
7. **Push to your fork**: `git push origin feature/your-feature-name`
8. **Create a Pull Request** with detailed description

## Development Setup

```bash
# Clone repository
git clone https://github.com/mldatascientist23/Dutch-AI-Voice-Assistant.git
cd Dutch-AI-Voice-Assistant

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install pytest pytest-asyncio

# Copy environment template
cp .env.example .env

# Configure with your settings
```

## Code Style

- Follow PEP 8
- Use clear, descriptive variable names
- Keep functions focused and concise
- Add comments for complex logic
- Use type hints in function signatures

## Testing

```bash
# Run all tests
cd backend
pytest tests/ -v

# Run specific test
pytest tests/test_api.py::test_create_call -v

# Run with coverage
pytest tests/ -v --cov=backend
```

## Commit Messages

- Use clear, descriptive messages
- Start with action verb (Add, Fix, Update, etc.)
- Limit first line to 50 characters
- Reference issues when applicable: "Fix #123"

## Areas for Contribution

- Bug fixes and improvements
- Documentation enhancements
- Test coverage expansion
- Performance optimizations
- New voice profiles or conversation flows
- Frontend UI/UX improvements
- Docker and deployment improvements

## Questions?

Feel free to open an issue for any questions or discussions related to the project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing!
