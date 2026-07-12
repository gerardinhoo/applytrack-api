# ApplyTrack API Reliability Objectives

## Purpose

ApplyTrack API is a portfolio backend service and hands-on reliability lab.

The following objectives demonstrate how user-focused reliability would be
defined and measured for the API. They are learning targets and do not imply
that the service currently handles continuous production traffic.

## Measurement window

All SLOs use a rolling 30-day measurement window.

## SLI 1: Availability

### Definition

The percentage of valid API requests that complete without a server-side
HTTP 5xx response.

Expected client responses such as HTTP 400, 404, and 422 are not treated as
availability failures because the API handled those requests correctly.

### SLO

At least 99% of valid API requests should complete without a 5xx response
over a rolling 30-day period.

### Measurement

Availability ratio:

successful requests / total requests

where successful requests are requests whose status code is not 5xx.

## SLI 2: Request latency

### Definition

The time between the API receiving a request and returning its HTTP response.

### SLO

At least 95% of API requests should complete in less than 500 milliseconds
over a rolling 30-day period.

### Reasoning

ApplyTrack is a small CRUD API that communicates with a remotely hosted
PostgreSQL database. A 500 millisecond p95 target is realistic for a learning
project without making unsupported performance claims.

## SLI 3: Server error rate

### Definition

The percentage of API requests that return an HTTP 5xx response.

### SLO

Fewer than 1% of API requests should return a 5xx response over a rolling
30-day period.

### Measurement

Server error ratio:

5xx responses / total responses

## Error budget

The availability SLO is 99%.

This permits an unsuccessful-request budget of:

1% of all valid API requests during the 30-day measurement window.

For a time-based approximation:

30 days × 24 hours × 60 minutes = 43,200 minutes

43,200 minutes × 1% = 432 minutes

Therefore, the approximate monthly error budget is:

7 hours and 12 minutes

This does not mean the service should intentionally be unavailable for that
amount of time. It represents the maximum tolerated unreliability before
reliability work should take priority over nonessential feature work.

## Error-budget policy

If ApplyTrack consumes most or all of its error budget:

1. Pause nonessential feature work.
2. Review recent deployments and failures.
3. Identify routes contributing to errors or latency.
4. Prioritize reliability fixes.
5. Resume feature work when reliability returns to an acceptable trend.

## Limitations

ApplyTrack does not currently receive continuous production traffic.

The metrics, SLOs, and error budget are intended to demonstrate practical SRE
concepts using honest, measurable targets.