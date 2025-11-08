# Contributing to SAES

Thank you for considering contributing to **SAES** (Stochastic Algorithm Evaluation Suite)! We welcome contributions that improve the tool, whether it's new features, bug fixes, documentation improvements, or enhancements. By contributing, you help make this project better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)
- [Community](#community)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## Getting Started

1. **Fork the Repository**: Click the "Fork" button at the top right of the repository page.
2. **Clone Your Fork**: 
   ```bash
   git clone https://github.com/YOUR-USERNAME/SAES.git
   cd SAES
   ```
3. **Add Upstream Remote**:
   ```bash
   git remote add upstream https://github.com/jMetal/SAES.git
   ```

## Development Setup

### Prerequisites

- Python >= 3.10
- pip (Python package installer)
- git

### Setting Up Your Development Environment

We use [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or with pip
   pip install uv
   ```

2. **Create a Virtual Environment and Install Dependencies**:
   ```bash
   # Create virtual environment
   uv venv
   
   # Activate it
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install the package with all dev dependencies
   uv pip install -e ".[dev]"
   ```

3. **Install Pre-commit Hooks** (Optional but Recommended):
   ```bash
   pre-commit install
   ```

#### Alternative: Traditional pip/venv

If you prefer traditional tools:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.plots.test_boxplot

# Run with coverage
coverage run -m unittest discover tests
coverage report
coverage html  # Generate HTML coverage report
```

### Building Documentation

```bash
cd docs
make html
# Open docs/_build/html/index.html in your browser
```

## How to Contribute

### Types of Contributions

1. **Bug Fixes**: Fix issues reported in the issue tracker.
2. **New Features**: Implement new statistical tests, visualizations, or utilities.
3. **Documentation**: Improve or add documentation, examples, and tutorials.
4. **Tests**: Add or improve test coverage.
5. **Performance**: Optimize existing code for better performance.

### Contribution Workflow

1. **Create a New Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bug/issue-number-description
   ```

2. **Make Your Changes**: Write your code, following the [Coding Standards](#coding-standards).

3. **Write Tests**: Add tests for your changes in the `tests/` directory.

4. **Update Documentation**: Update relevant documentation if needed.

5. **Run Tests**: Ensure all tests pass.
   ```bash
   python -m unittest discover tests
   ```

6. **Commit Your Changes**: Use clear, descriptive commit messages.
   ```bash
   git commit -m "feat: add new Bayesian posterior analysis feature"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for adding tests
   - `refactor:` for code refactoring
   - `style:` for formatting changes
   - `perf:` for performance improvements

7. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**: Go to the original repository and click "New Pull Request".

## Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows the project's style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear and follow conventions
- [ ] Branch is up to date with main branch

### PR Description Should Include

1. **Summary**: Brief description of what the PR does
2. **Motivation**: Why is this change needed?
3. **Changes**: List of main changes made
4. **Testing**: How was this tested?
5. **Screenshots** (if applicable): For UI/visualization changes
6. **Breaking Changes**: Clearly note any breaking changes
7. **Related Issues**: Link to related issue(s) using `#issue-number`

### Example PR Title

```
feat: add support for custom color schemes in boxplots
```

### Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Once approved, your PR will be merged
- **One Change Per PR**: Keep PRs focused on a single feature or fix

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length: 120 characters
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of the function.

    Detailed description if necessary.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When invalid input is provided.

    Example:
        >>> from SAES.module import function_name
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Code Formatting

The project uses the following tools (automatically applied if pre-commit is installed):

- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting

To manually format code:
```bash
black SAES tests
isort SAES tests
flake8 SAES tests
```

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the package structure in test files
- Use descriptive test names: `test_<function>_<scenario>`
- Test both expected behavior and edge cases
- Include tests for error conditions

### Test Example

```python
import unittest
from SAES.statistical_tests.non_parametrical import friedman

class TestFriedman(unittest.TestCase):
    def setUp(self):
        self.data = ...  # Test data
    
    def test_friedman_basic_functionality(self):
        """Test basic friedman test execution."""
        result = friedman(self.data, maximize=True)
        self.assertIsInstance(result, pd.DataFrame)
        # More assertions...
    
    def test_friedman_invalid_input(self):
        """Test friedman with invalid input."""
        with self.assertRaises(ValueError):
            friedman(invalid_data, maximize=True)
```

## Documentation

### Documentation Standards

- Document all public APIs
- Include usage examples
- Update relevant `.rst` files in `docs/`
- Add entries to appropriate documentation sections

### Building and Viewing Documentation Locally

```bash
cd docs
make html
open _build/html/index.html  # macOS
# or
xdg-open _build/html/index.html  # Linux
# or
start _build/html/index.html  # Windows
```

## Reporting Issues

### Before Creating an Issue

- Search existing issues to avoid duplicates
- Check the documentation
- Try to reproduce the issue

### Creating a Good Issue

Include:

1. **Clear Title**: Descriptive and specific
2. **Environment**:
   - OS and version
   - Python version
   - SAES version
3. **Steps to Reproduce**: Minimal code example
4. **Expected Behavior**: What should happen
5. **Actual Behavior**: What actually happens
6. **Additional Context**: Screenshots, error messages, etc.

### Issue Templates

Use the appropriate template when available:
- Bug Report
- Feature Request
- Documentation Improvement

## Community

### Getting Help

- **Documentation**: Check the [official documentation](https://jMetal.github.io/SAES/)
- **Issues**: Search or create an issue
- **Discussions**: Join GitHub Discussions for questions and ideas

### Stay Updated

- Watch the repository for updates
- Follow release notes in CHANGELOG.md
- Check the project roadmap

## Recognition

Contributors will be acknowledged in:
- Release notes
- CHANGELOG.md
- GitHub contributors page

## License

By contributing to SAES, you agree that your contributions will be licensed under the GNU General Public License v3.0.

---

## Thank You! 🎉

Your contributions help make SAES better for everyone. We appreciate your time and effort in helping to improve the project!

For questions about contributing, please open an issue or contact the maintainers directly.
