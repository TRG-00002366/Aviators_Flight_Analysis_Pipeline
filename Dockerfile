# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.14

WORKDIR /app

RUN apt-get update && apt-get install -y \
    openjdk-21-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev 

COPY . .

CMD ["uv", "run", "src/infra/setup_kafka.py"]