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
