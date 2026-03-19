#!/bin/bash
uv run python -m src.infra.Producer
spark-submit src/infra/spark_streaming_consumer.py
