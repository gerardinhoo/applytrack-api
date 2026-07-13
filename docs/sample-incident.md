# Sample Incident: Elevated HTTP 5xx Errors

## Summary

While testing the ApplyTrack API, I intentionally generated server errors to verify the Prometheus metrics and Grafana dashboards.

## Impact

Users would have received temporary HTTP 500 responses.

## Detection

The HTTP 5xx Error Rate panel immediately showed increased errors.

The Request Rate panel confirmed incoming traffic.

The Total HTTP Requests panel continued increasing.

## Root Cause

Intentional testing.

## Resolution

Stopped generating failing requests.

Error rate returned to zero.

## Lessons Learned

- Prometheus correctly collected metrics.
- Grafana visualized the errors.
- Dashboards successfully detected application failures.