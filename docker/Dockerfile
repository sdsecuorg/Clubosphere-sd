FROM python:3.13-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root
RUN poetry run python -c "import pymongo; print(pymongo.__version__)"
COPY . .

EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["poetry", "run", "python", "run.py"]
