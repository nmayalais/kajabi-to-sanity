# Contributing to Kajabi to Sanity Migration Tool

First off, thank you for considering contributing to this project! 

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment details (Python version, OS, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear and descriptive title
- A detailed description of the proposed feature
- Any relevant examples or use cases
- Why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add or update tests as needed
5. Update documentation if required
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/[your-username]/kajabi-to-sanity.git
cd kajabi-to-sanity
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Coding Standards

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Write clear, self-documenting code

## Testing

Before submitting a PR:

1. Test your changes with different Kajabi sites if possible
2. Ensure all existing functionality still works
3. Add unit tests for new features
4. Run the tool with `--log-level DEBUG` to check for issues

## Documentation

- Update the README.md if you change functionality
- Add inline comments for complex logic
- Update command-line help text if adding new options

## Questions?

Feel free to open an issue for any questions about contributing!