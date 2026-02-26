# Aviators Project: Flight Analysis Pipeline
## Overview
Our Data Engineering project is a real-time streaming data pipeline which ingests real-time flight events
via Kafka from the OpenSky API, processes them via Pyspark, and orchestrates the entire workflow using Apache Airflow.
## Business Scenario
The FAA wants to:
1. **Stream** flight events (longitutde, latitude, transponder) in real time
2. **Process** the raw events to compute the following:
    -   Flight Density of a Given Airspace
    -   Distribution of Aircraft and Flight Types (long range, short range, Airbus, Boeing, etc.)
    -   Airline activity by region 
3. **Persist** both raw and transformed data to storage (S3)
4. **Orchestrate** the batch and streaming jobs on a daily schedule with retry and alerting


- For our project spec, what do you expect by Monday?

## Analytics
- Flight Density of Given Airspace
    - Return how many airplanes are in a certain area
- Distribution of Aircraft and Flight Types
    - Return the different types of aircraft