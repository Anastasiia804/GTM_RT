# Contributing to TSPRTG Tag Manager

Thank you for your interest in contributing to TSPRTG Tag Manager!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/GTM_RT.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`
4. Follow the installation instructions in README.md

## Making Changes

### Backend Changes

- All backend code is in the `backend/` directory
- Follow PEP 8 style guidelines for Python code
- Add docstrings to new functions and classes
- Update API documentation in README.md if needed

### Frontend Changes

- All frontend code is in the `frontend/` directory
- Use Vue 3 Composition API
- Follow existing component structure
- Ensure responsive design

### Database Changes

- Modify models in `backend/app/models/`
- Update schemas in `backend/app/schemas/`
- Test migrations thoroughly

## Testing

Before submitting a PR:

1. Test backend endpoints:
   ```bash
   ./test-api.sh
   ```

2. Test frontend build:
   ```bash
   cd frontend
   npm run build
   ```

3. Test with Docker:
   ```bash
   docker-compose up --build
   ```

## Submitting Pull Requests

1. Ensure your code follows the project style
2. Update documentation as needed
3. Add meaningful commit messages
4. Create a pull request with:
   - Clear title and description
   - Reference any related issues
   - List of changes made
   - Screenshots for UI changes

## Code Review Process

- All PRs require review before merging
- Address review feedback promptly
- Keep PRs focused on a single feature/fix

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase

Thank you for contributing!
