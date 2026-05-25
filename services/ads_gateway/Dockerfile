FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY libs /app/libs
COPY services/ads_gateway /app/services/ads_gateway

RUN pip install --no-cache-dir fastapi "uvicorn[standard]" pydantic python-dotenv httpx "psycopg[binary]"

EXPOSE 8000

CMD ["uvicorn", "services.ads_gateway.app.main:app", "--host", "0.0.0.0", "--port", "8000"]