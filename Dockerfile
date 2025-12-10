FROM python:3.10-slim AS builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . .

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-root 


FROM python:3.10-slim AS final

WORKDIR /app


COPY --from=builder /app/.venv /app/.venv 
COPY --from=builder /app ./

EXPOSE 8000

RUN pip install poetry
ENV PATH="/root/.local/bin:${PATH}"

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]