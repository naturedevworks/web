#기술 스택
frontend 폴더에 vue 프로젝트로 프론트엔드 개발
app 폴더에 fastapi 프로젝트로 백엔드 개발
DB는 SQLlite로  app.db 파일로 관리


#검증
백엔드는 pytest 로 테스트 할 수 있는 테스트 코드 작성 후 전체 통과되면 완료
프론트앤드는  jest로 테스트할 수 있는 테스트 코드 작성 후 전체 통과되면 완료

# Persistent subagent roles

Use these role definitions in future Codex sessions when work calls for specialist agents:

- `backend-dev.toml`: backend work in `app/`, using the existing FastAPI project structure.
- `frontend-dev.toml`: frontend work in `frontend/`, using the existing Vue structure and Axios for backend API calls.

Subagents are session-scoped and do not remain running after a session ends. In each new session, spawn the relevant role again and give it the current task; spawn both when backend and frontend work can proceed independently. The role files are the durable source of their instructions.

Repository verification instructions conflict: the user-provided AGENTS instructions say to skip tests, while the project note says to add and pass backend pytest or frontend Jest tests. Follow the latest direct user instruction for the task; at present, do not run tests unless the user asks.

# Deployment memory

- Frontend is served by Nginx on the Windows server `100.100.100.101`, installed at `C:\nginx-1.30.5` (web root `C:\nginx-1.30.5\html`).
- Backend is served by Uvicorn on the separate Windows server `100.100.100.102`, deployed to `C:\backend` (HTTPS application port `443`, using the certificate and key under `C:\backend\certs`).
- SSH account on both servers: `test`. Keep the supplied password only in GitHub Actions secrets; never write it to repository files or logs.
- Production frontend/API URLs are `https://www.naturedevworks.kro.kr` and `https://api.naturedevworks.kro.kr`. Do not use localhost in production builds or deployment settings.
