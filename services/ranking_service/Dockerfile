FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY libs /app/libs
COPY services /app/services

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic python-dotenv

EXPOSE 8007

CMD ["uvicorn", "services.ranking_service.app.main:app", "--host", "0.0.0.0", "--port", "8007"]