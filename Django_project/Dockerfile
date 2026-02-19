# 1. 파이썬 3.14 이미지 기반
FROM python:3.14-slim

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# uv가 설치되는 경로를 PATH에 추가
ENV PATH="/root/.local/bin:${PATH}"

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 먼저 복사
COPY ./pyproject.toml ./uv.lock* ./

# 패키지 설치 (lock 파일이 없을 수도 있으니 에러 방지)
RUN uv sync --all-packages

# [중요] 애플리케이션 전체 코드 복사 (manage.py 등이 포함되도록)
COPY . .

# 스크립트 실행 권한 부여 (scripts 폴더가 있다면)
RUN chmod +x /app/scripts/*.sh 2>/dev/null || true

# 포트 설정
EXPOSE 8000

# Django 개발 서버 실행 (설정 파일 경로 명시)
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=config.settings.dev"]