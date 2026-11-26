# Contributing to Asahi

Thank you for considering contributing to Asahi! This project helps people manage their mental wellness through daily check-ins and personalized missions. Here's how you can help:

## Development Setup

1. **Fork the repository** and clone your fork locally
2. **Install dependencies**:
   ```bash
   # Frontend
   cd frontend
   npm install

   # Backend
   cd backend
   pip install -r dependencies/requirements.txt
   ```

3. **Set up environment variables** - copy `.env.example` and fill in your values
4. **Run the development servers**:
   - Frontend: `cd frontend && npm run dev`
   - Backend: `cd backend && uvicorn main:app --reload`

## Project Structure

```
asahi/
├── frontend/          # React + TypeScript + Vite
│   ├── src/           # Source code
│   ├── vite.config.ts # Vite config
│   └── index.html
│
├── backend/           # FastAPI + Python
│   ├── main.py        # FastAPI app entry point
│   ├── core/          # Database, security, config
│   ├── models/        # SQLAlchemy models
│   ├── routes/        # API endpoints
│   ├── ml/            # Machine learning models
│   └── mission/       # Mission recommendation engine
│
├── alembic/           # Database migrations
├── scripts/           # Seed data and utilities
└── docs/              # Documentation
```

## Code Style

- **Frontend**: Follow the existing code patterns in the React + TypeScript codebase. Use ESLint for linting.
- **Backend**: Follow Python best practices, use type hints where appropriate, and adhere to the existing code style.
- **Commits**: Write clear, descriptive commit messages. Follow the existing commit message format in the repository.

## Testing

- Run the test suite: `cd backend && python -m pytest`
- Ensure all existing tests pass before submitting changes
- Add new tests for any new functionality you introduce

## Pull Request Process

1. Create a new branch from `main` for your feature or bug fix
2. Make your changes and ensure tests pass
3. Submit a pull request with a clear description of what you changed and why
4. Address any feedback from maintainers

## Reporting Issues

- Use the [GitHub Issues](https://github.com/your-org/asahi/issues) tracker
- Include a clear title and description
- For bugs, include steps to reproduce and expected vs. actual behavior
- For feature requests, explain the problem you're trying to solve

## Thank You!

Your contributions help make Asahi better for everyone. Every bug fix, improvement, and new feature brings us closer to supporting more people on their mental wellness journey.