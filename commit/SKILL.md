---
name: commit
description: Create a git commit with a conventional commit message based on staged or unstaged changes.
disable-model-invocation: true
allowed-tools: Bash
---

Create a git commit for the current changes.

## Instructions

1. Run `git status` to check current changes
2. Run `git diff` and `git diff --staged` to understand all modifications
3. Generate a commit message following **Conventional Commits** format:

## Commit message format

```
<type>(<scope>): <subject>

<body>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring (no feature change, no bug fix)
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `chore`: Build, CI, dependency updates
- `perf`: Performance improvement
- `style`: Code style changes (formatting, semicolons, etc.)

### Rules
- Subject line: max 50 characters, imperative mood, no period
- Body: explain WHAT and WHY, not HOW
- Scope: the module or component affected
- Stage only relevant files (avoid staging .env, credentials, or unrelated files)

## Process
1. Show the proposed commit message to the user
2. Stage the relevant files
3. Create the commit
