# Aviators Project: Flight Analysis Pipeline
## Overview
Our Data Engineering project is a real-time streaming data pipeline which processes simulated real-time flight events.
## Business Scenario
The FAA is moderating an en-route airspaace and wants to:
1. **Stream** flight events (longitutde, latitude, transponder, etc) in real time
2. **Process** the raw events to compute some of the following:
    -   Flight Density of a Given Airspace
    -   Distribution of Aircraft and Flight Types (long range, short range, Airbus, Boeing, etc.)
    -   Airline activity by region 
    -   Squawk codes
    -   Proxmitiy and separaton violations
    -   Sector congestion
    -   Dwell time
3. **Persist** both raw and transformed data to storage (S3)
4. **Orchestrate** the batch and streaming jobs on a daily schedule with retry and alerting
## General Model
- Predefined En-Route Airspace
- New flights appear as aircraft entering the airspace
- Flight data is updated as aircraft cross the airspace
- Flights "disappear" as they leave the airspace
## Flight Schema
``` JSON
{
  "flight_id": "FLT-0001",
  "callsign": "UAL3CC",
  "aircraft_type": "B787",
  "longitude": "74.0060° W",
  "latitude": "40.7128° N",
  "elevation": "2000 f.t.",
  "speed_kt": "100",
  "heading": "330",
  "squawk": "2345",
  "timestamp": "2026-03-01T12:34:56Z"
}
```