# Contributing to FastAPI Boilerplate

First off, thank you for considering contributing to FastAPI Boilerplate! It's people like you who make the open-source community such an amazing place to learn, inspire, and create.

## How Can I Contribute?

### Reporting Bugs
*   Check the [GitHub Issues](https://github.com/yourusername/fastapi_boilerplate/issues) to see if the bug has already been reported.
*   If not, open a new issue. Include a clear title and a detailed description with as much relevant information as possible, including steps to reproduce the bug.

### Suggesting Enhancements
*   Open a new issue with the tag "enhancement".
*   Explain why this enhancement would be useful to most users.

### Pull Requests
1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/amazing-feature`).
3.  Make your changes.
4.  Ensure your code follows the coding standards (run `ruff check .` and `mypy .`).
5.  Add tests for your changes.
6.  Ensure all tests pass (`pytest`).
7.  Commit your changes (`git commit -m 'Add some amazing feature'`).
8.  Push to the branch (`git push origin feature/amazing-feature`).
9.  Open a Pull Request.

## Coding Standards
*   We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.
*   We use [Mypy](https://github.com/python/mypy) for static type checking.
*   Follow PEP 8 guidelines.
*   Write clear, descriptive commit messages.

## Environment Setup
1.  Clone the repo.
2.  Create a virtual env: `python -m venv venv`.
3.  Install dev dependencies: `pip install -e ".[dev]"`.
4.  Copy `.env.example` to `.env` and configure.
5.  Start Docker: `docker-compose up -d`.

## License
By contributing, you agree that your contributions will be licensed under its MIT License.
