# 1. 파이썬 3.14 이미지를 기반으로 시작 (만약 에러나면 3.12-slim으로 변경 권장)
FROM python:3.14-slim

# 2. uv 설치
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일 먼저 복사 (캐싱 효율을 위해)
COPY pyproject.toml uv.lock ./

# 5. 패키지 설치
RUN uv sync --frozen

# 6. 나머지 프로젝트 코드 복사
COPY . .

# 7. 장고 서버 실행 (config.settings.dev 설정 사용)
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=config.settings.dev"]