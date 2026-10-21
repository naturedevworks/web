# Windows 서버 배포

## 배포 흐름

- `frontend/**`가 `main`에 반영되면 GitHub Actions가 production 빌드를 만들고 Nginx 웹 루트에 업로드합니다.
- `app/**`, `main.py` 또는 `requirements.txt`가 `main`에 반영되면 GitHub Actions가 백엔드 파일을 `C:\backend`에 반영하고 Uvicorn을 재시작합니다.
- 프론트엔드 API 주소는 `frontend/.env.production` 한 곳에서 관리합니다. 운영 주소는 `https://api.naturedevworks.kro.kr`입니다.
- 브라우저는 `https://www.naturedevworks.kro.kr`에서 API를 호출합니다. 백엔드는 이 정확한 Origin에 대해 CORS credentials 요청을 허용합니다.
- 인증 쿠키는 API 호스트 전용으로 발급합니다(`Domain` 속성 생략). 브라우저는 프론트엔드 JavaScript가 쿠키를 읽지 않아도 `credentials: include`가 설정된 API 요청에 쿠키를 보냅니다. `Domain=www.naturedevworks.kro.kr`는 API 호스트의 형제 도메인이어서 브라우저가 거부합니다. Production 쿠키는 `Secure`, `HttpOnly`, `SameSite=None`로 발급되며 두 주소 모두 HTTPS여야 합니다.

## GitHub Actions 설정

저장소의 **Settings → Secrets and variables → Actions**에서 다음 Repository secrets를 등록합니다. IP, SSH 포트, 계정, 비밀번호는 파일에 저장하지 않습니다.

| Secret 이름 | 값 |
| --- | --- |
| `FRONTEND_SSH_HOST` | `100.100.100.101` |
| `FRONTEND_SSH_PORT` | 프론트엔드 Windows 서버의 SSH 포트 (보통 `22`) |
| `FRONTEND_SSH_USER` | 프론트엔드 서버 SSH 계정 |
| `FRONTEND_SSH_PASSWORD` | 프론트엔드 서버 SSH 비밀번호 |
| `BACKEND_SSH_HOST` | `100.100.100.102` |
| `BACKEND_SSH_PORT` | 백엔드 Windows 서버의 SSH 포트 (보통 `22`) |
| `BACKEND_SSH_USER` | 백엔드 서버 SSH 계정 |
| `BACKEND_SSH_PASSWORD` | 백엔드 서버 SSH 비밀번호 |

선택적으로 다음 Repository variables를 설정할 수 있습니다.

| Variable 이름 | 기본값 | 용도 |
| --- | --- | --- |
| `FRONTEND_NGINX_ROOT` | `/c/nginx-1.30.5/html` | Nginx 웹 루트. Windows 경로를 Git Bash 형식으로 입력합니다. |
| `BACKEND_DEPLOY_PATH_GIT_BASH` | `/c/backend` | SCP 업로드 경로. Windows 경로를 Git Bash 형식으로 입력합니다. |
| `BACKEND_DEPLOY_PATH_WINDOWS` | `C:\backend` | 백엔드 배포 경로의 Windows 형식 |
| `BACKEND_APP_PORT` | `443` | Uvicorn HTTPS 포트 |
| `DEPLOY_RUNNER_LABEL` | `deploy-network` | SSH 네트워크에 접근 가능한 GitHub Actions runner의 라벨 |

`FRONTEND_SSH_PORT`와 `BACKEND_SSH_PORT`는 SSH 포트입니다. Uvicorn의 HTTPS 앱 포트 `443`과는 별개입니다. 새 Windows 서버가 기본값 `22`를 사용하지 않는다면 각 SSH 포트를 실제 값으로 등록해야 합니다.

## Windows 서버 준비

두 Windows 서버에 Git for Windows를 설치하고 OpenSSH 서버의 기본 셸을 Git Bash로 설정해야 합니다. `appleboy/scp-action`은 Windows 대상으로 `/c/...` 형식의 경로를 사용하며, Git Bash 셸을 요구합니다. SSH 계정에는 배포 경로 쓰기 권한이 필요합니다.

백엔드 서버에는 Python 3와 `py` launcher 또는 `python` 명령이 설치되어야 합니다. SSH 계정에는 Uvicorn 프로세스를 멈추고 다시 시작할 권한이 필요합니다. HTTPS 인증서와 키는 서버의 `C:\backend\certs\certificate.crt`, `C:\backend\certs\private.key`에 둡니다. 배포 스크립트는 기존 Uvicorn만 멈춘 뒤 해당 인증서로 `0.0.0.0:443`에 Uvicorn을 실행하고, 로컬 HTTPS `/openapi.json` 응답을 확인합니다. 실행 로그는 `C:\backend\logs\uvicorn.stdout.log`와 `C:\backend\logs\uvicorn.stderr.log`에 저장됩니다. 서버의 `C:\backend\.env`, `C:\backend\certs`, `C:\backend\app.db`는 배포 과정에서 덮어쓰거나 삭제하지 않습니다.

프론트엔드 서버의 기본 웹 루트는 `C:\nginx-1.30.5\html`입니다. 빌드된 `index.html`과 asset 파일을 해당 경로로 덮어씁니다. 정적 파일 배포는 Nginx 재시작 없이 반영됩니다.

## 네트워크 접근 조건

`100.100.100.x` 주소는 공용 인터넷에서 일반적으로 라우팅되지 않는 공유 주소 대역(`100.64.0.0/10`)입니다. GitHub-hosted runner는 이 서버에 바로 접속할 수 없으므로 기본적으로 `deploy-network` label이 붙은 Linux self-hosted runner에서 배포하도록 설정했습니다. 그 runner는 두 Windows 서버와 같은 VPN/사내 네트워크에 연결되어 있어야 하고 Docker 컨테이너 액션을 실행할 수 있어야 합니다. Node.js 다운로드와 `npm ci`를 위해 GitHub 및 npm registry로도 나갈 수 있어야 합니다. 다른 label을 쓰면 `DEPLOY_RUNNER_LABEL` Actions variable에 넣으세요. GitHub-hosted runner를 사용하려면 별도로 사설 네트워크 경로를 구성해야 합니다.

## 배포 후 확인

프론트엔드 workflow는 생성된 bundle 안에서 `https://api.naturedevworks.kro.kr`가 있는지 확인하고 `localhost:8000`이 남아 있으면 업로드를 중단합니다. Actions 실행이 성공한 뒤 브라우저 개발자 도구에서 API Request URL, `Set-Cookie` 응답, 다음 `/auth/me` 요청의 Cookie 헤더를 확인합니다. `Referrer policy`는 API 주소 설정과 무관합니다.


## Frontend IP access

The API also allows the exact frontend origin https://100.100.100.101 for direct IP access. Production authentication and OAuth state cookies use SameSite=None; Secure so credentialed API calls can work from this cross-site origin. Use HTTPS for both frontend and API. The canonical https://www.naturedevworks.kro.kr origin remains supported.
