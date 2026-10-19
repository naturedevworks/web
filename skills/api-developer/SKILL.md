---
name: api-developer
description: Implement and maintain FastAPI endpoints in this repository's app/ backend, following its documented module layout and SQLite app.db conventions; add pytest coverage for API behavior.
metadata:
  short-description: Build and test this project's FastAPI endpoints
---

# API Developer

Use this skill for backend API work in this repository. The frontend lives in `frontend/`; backend code belongs in `app/`. The documented target layout is:

```text
app/
  main.py
  core/       # configuration and security
  db/         # database connection and session
  models/     # database models
  schemas/    # request and response schemas
  api/
    deps.py   # shared dependencies
    routers/  # endpoint routers
```

The `app/` directory may not yet contain this layout. Inspect existing files and project dependencies before implementing; create only the modules needed for the requested feature and keep existing conventions when they differ. SQLite is the project's database and `app.db` is its application database file. Do not assume an ORM or authentication scheme until dependency files and existing code establish it.

## Workflow

1. Read repository `AGENTS.md`, backend-specific instructions, `docs/프로젝트 구조.txt`, relevant API requirements, and the existing `app/` code. Treat explicit user requirements and applicable project instructions as controlling.
2. For non-trivial API engineering work, load `postman:api-engineer` and follow its routing guidance. Use specialized Postman workflows only when the task needs them; do not publish, deploy, or mutate shared workspaces unless explicitly requested.
3. Define the endpoint contract from the requested behavior: method and path, input and output schemas, status codes, validation, error cases, and authentication/authorization requirements. Preserve established API conventions and avoid unrelated changes.
4. Implement the endpoint in the appropriate router, define Pydantic schemas and persistence models as needed, wire dependencies through `app/main.py`, and use shared database/session dependencies. Keep SQLite-specific behavior compatible with the project setup.
5. Add pytest tests for success, validation failures, relevant missing/duplicate records, and authorization or error cases that apply. Exercise the API through FastAPI's test client using isolated test data and a temporary/test database or dependency overrides; never let tests mutate the developer's `app.db` or a production database.
6. Run the applicable pytest suite when repository instructions permit. If instructions say to skip test execution, still write the requested tests and report that they were not run. Fix failures caused by the change; distinguish pre-existing failures from new ones.
7. Summarize changed files, endpoint behavior, test coverage, and test execution result. Do not claim tests passed unless they were run and passed.

## Implementation guidance

- Keep transport concerns in routers, validation and serialization in schemas, persistence in models/database modules, and shared request dependencies in `api/deps.py` where the existing architecture supports that separation.
- Use explicit response models and meaningful HTTP status codes. Return consistent error details without leaking secrets or internal exceptions.
- Validate input at the schema boundary and enforce business rules in the appropriate application layer. Handle uniqueness and transaction errors safely, including SQLite integrity constraints where relevant.
- Store passwords only as secure password hashes when implementing account flows; never log credentials or return stored hashes.
- Keep configuration and secrets out of source code. Preserve the documented `app.db` location while ensuring tests use an isolated database.
- Avoid adding dependencies when the existing stack can meet the requirement. If a dependency is necessary, update the repository's dependency manifest in the established way.
