# ApplyTrack API

ApplyTrack is a FastAPI backend for tracking job applications. It combines a PostgreSQL-backed CRUD API with Docker, automated testing, a historical Google Kubernetes Engine (GKE) deployment, and local Prometheus/Grafana observability.

The API stores job applications with a company, position, and status. Data is persisted through SQLAlchemy, with Pydantic validating incoming requests.

## What This Project Demonstrates

- Python, FastAPI, Pydantic, SQLAlchemy, and PostgreSQL
- Docker and Docker Compose
- Historical deployment to GKE through Google Cloud Build
- Kubernetes Deployment, LoadBalancer Service, liveness probe on `/health`, readiness probe on `/ready`
- Prometheus instrumentation at `/metrics`
- Prometheus and Grafana run locally through Docker Compose
- Grafana dashboard-as-code
- Documented SLIs, SLOs, and error-budget analysis in `docs/slos.md`

This is a backend/cloud/reliability engineering project, not a claim of continuous production operation.

## Known Limitations / Scope

- No authentication or authorization
- No Kubernetes Ingress; external access used a LoadBalancer Service
- Prometheus and Grafana are local through Docker Compose, not deployed on GKE
- No HPA, PDB, NetworkPolicy, or in-cluster monitoring stack
- SLOs and error budgets are documented reliability targets supported by metrics, not an automated production SLO system
- No automated error-budget burn alerts or on-call process
- The GKE cluster was intentionally deleted after validation to control cloud cost
- No continuous production traffic

## Tech Stack

| Category | Technologies |
| --- | --- |
| Backend | Python, FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic |
| Database | PostgreSQL, Neon |
| Testing | pytest, FastAPI TestClient, SQLite test database |
| Containers | Docker, Docker Compose |
| Cloud and CI/CD | GitHub Actions, Google Cloud Build, Container Registry, Google Cloud |
| Kubernetes | GKE, Deployment, LoadBalancer Service, probes, resources, Secrets |
| Observability | Prometheus, Grafana, `prometheus-fastapi-instrumentator`, PromQL |

## Architecture

```mermaid
flowchart LR
    developer["Developer push"] --> github["GitHub repository"]
    github --> cloudbuild["Google Cloud Build"]
    cloudbuild --> registry["Container image registry"]
    registry --> deployment["GKE Deployment"]
    deployment --> service["Kubernetes LoadBalancer Service"]
    service --> api["FastAPI"]
    api --> neon["Neon PostgreSQL"]

    api --> metrics["/metrics"]
    metrics --> prometheus["Prometheus (local Compose)"]
    prometheus --> grafana["Grafana (local Compose)"]

    deployment -.-> cleanup["GKE cluster deleted after validation to control cost"]
```

The GKE path was deployed and tested successfully. The cluster was later deleted, so the diagram describes the validated deployment architecture rather than a currently live public service.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Return the API status message |
| `GET` | `/health` | Liveness check; process is alive, no database dependency |
| `GET` | `/ready` | Readiness check; verifies database connectivity |
| `GET` | `/applications` | List all job applications |
| `POST` | `/applications` | Create a job application |
| `GET` | `/applications/{application_id}` | Retrieve one job application |
| `PUT` | `/applications/{application_id}` | Replace an existing job application's fields |
| `DELETE` | `/applications/{application_id}` | Delete a job application |
| `GET` | `/metrics` | Expose Prometheus-compatible application metrics |

### Optional test endpoint

`GET /test-error` intentionally returns HTTP 500 only when `ENABLE_TEST_ENDPOINTS=true`. The setting defaults to `false`; when disabled, the route returns HTTP 404. Keep it disabled in shared and cloud environments. Use it only for controlled local monitoring exercises.

## Running Locally

A PostgreSQL database is required. Create a local `.env` file from `.env.example`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/applytrack
```

Replace the placeholder with your real local or Neon connection string. Do not commit `.env`.

Add `ENABLE_TEST_ENDPOINTS=true` only when running the controlled failure exercise locally.

### Database migrations

Apply the versioned schema before starting the API:

```bash
alembic upgrade head
```

For a pre-existing ApplyTrack database whose `applications` table already matches the initial migration, review the schema and record the baseline once without recreating the table:

```bash
alembic stamp head
```

`stamp` records the revision but does not change the schema. Use it only for an existing matching database. New or empty databases should use `alembic upgrade head`.

After changing a SQLAlchemy model, generate and review a migration before applying it:

```bash
alembic revision --autogenerate -m "describe the schema change"
alembic upgrade head
```

### Python virtual environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

On Windows PowerShell, activate the environment with `venv\Scripts\Activate.ps1`.

### Docker

```bash
docker build -t applytrack-api .
docker run --rm --env-file .env applytrack-api alembic upgrade head
docker run --env-file .env -p 8000:8000 applytrack-api
```

### Docker Compose

Docker Compose starts the API, Prometheus, and Grafana locally. The Prometheus data source and ApplyTrack dashboard are provisioned automatically when Grafana starts:

```bash
docker compose run --rm api alembic upgrade head
docker compose up --build
```

- API: <http://localhost:8000>
- Swagger UI: <http://localhost:8000/docs>
- Metrics: <http://localhost:8000/metrics>
- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>

## Testing

Run the test suite:

```bash
pytest
```

Tests override FastAPI's database dependency with an in-memory SQLite database, and the schema is recreated for every test. This prevents test records from reaching Neon and prevents state from leaking between tests.

The [GitHub Actions workflow](.github/workflows/ci.yml) runs on every push and pull request. It uses Python 3.12, installs the project dependencies, checks that the Python files compile, validates an Alembic upgrade/downgrade cycle, validates the Grafana dashboard JSON, and runs pytest. The CI job does not require a database secret because its migration check and tests use isolated SQLite databases.

## Reliability Objectives

The detailed [SLI, SLO, and error-budget definitions](docs/slos.md) cover three indicators:

- Availability: the ratio of valid requests that do not return HTTP 5xx, with a 99% SLO over a rolling 30-day window
- Latency: p95 request latency, with a target that at least 95% of requests complete in under 500 ms
- Server errors: the HTTP 5xx response ratio, with a target below 1%

These are documented reliability targets and analysis exercises. They are supported by Prometheus metrics and Grafana panels locally, but they are not enforced by an automated production SLO system, burn alerts, or on-call process. ApplyTrack does not receive continuous production traffic.

## Observability

FastAPI exposes Prometheus-compatible metrics at `/metrics`. In the local Compose environment, Prometheus scrapes the API every 15 seconds and Grafana reads the collected time series from Prometheus. The Prometheus data source and ApplyTrack dashboard are provisioned from version-controlled files under `monitoring/grafana/`. The instrumentation library normalizes route labels to templates such as `/applications/{application_id}`, which avoids separate labels for every resource ID.

Grafana panels include:

- Total HTTP Requests
- Request Rate
- p95 Request Latency
- HTTP 5xx Error Rate as a ratio of failed responses to all responses

Prometheus and Grafana are not deployed on GKE in this repository. Kubernetes saturation monitoring was outside the scope of this implementation.

## Failure Simulation

The environment-controlled `/test-error` route was used to generate known HTTP 500 responses during local monitoring exercises. During the exercise, the total-request, request-rate, latency, and 5xx panels reacted to the generated traffic.

This was a controlled failure simulation used for observability validation, not full chaos engineering. See the [sample incident report](docs/sample-incident.md).

## Deployment and CI/CD

The implemented delivery flow is:

```text
GitHub push
  -> Cloud Build trigger
  -> Docker image build
  -> commit SHA and latest tags
  -> image push
  -> deployment to GKE
```

[`cloudbuild.yaml`](cloudbuild.yaml) builds and pushes both an immutable `$SHORT_SHA` image and a convenience `latest` tag, then deploys the commit-specific image. [`gke.yaml`](gke.yaml) defines the one-replica Deployment, liveness probe on `/health`, readiness probe on `/ready`, compute resources, Secret reference, and LoadBalancer Service.

The pipeline and application were successfully tested on GKE. The cluster was subsequently deleted to control cloud costs, so no live public endpoint is advertised. The Cloud Build trigger may remain disabled while the target cluster does not exist.

## Application & Deployment Evidence

### FastAPI / OpenAPI

The Swagger UI exposes and documents the ApplyTrack API surface, including CRUD routes, health/readiness endpoints, and request schemas.

![ApplyTrack Swagger UI](ApplyTrack-Screenshots/apply-track-project-screenshots/swagger-ui.png)

### CI/CD — Cloud Build

Google Cloud Build built and pushed the container image, then deployed the workload to GKE using the commit-specific image tag.

![Successful Google Cloud Build deployment](ApplyTrack-Screenshots/apply-track-project-screenshots/cloud-build.png)

### Kubernetes — GKE

This historical deployment evidence shows the ApplyTrack workload running successfully in GKE. The cluster was intentionally deleted afterward to control cloud cost, so no live cluster remains today.

![ApplyTrack deployment in GKE](ApplyTrack-Screenshots/apply-track-project-screenshots/gke-deployment.png)

### Observability — Prometheus & Grafana

The FastAPI application exposes Prometheus metrics at `/metrics`. The local Docker Compose monitoring stack scrapes those metrics and visualizes request and error behavior in Grafana.

![Grafana HTTP 5xx error rate during controlled failure simulation](ApplyTrack-Screenshots/applyTrack-monitoring-observability/post-incident-simulation/http-error-rate.png)

Additional historical screenshots remain under `ApplyTrack-Screenshots/` but are not featured here.

## Repository Structure

```text
applytrack-api/
├── app/                  # FastAPI application, models, schemas, and routes
├── tests/                # API tests
├── docs/                 # Reliability objectives and sample incident
├── monitoring/           # Prometheus and provisioned Grafana configuration
├── alembic/              # Versioned database migrations
├── .github/workflows/    # GitHub Actions CI checks
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── cloudbuild.yaml
├── gke.yaml
├── LICENSE
├── SECURITY.md
└── README.md
```

## Cost-Conscious Cleanup

After deployment validation, the GKE cluster and its compute and load-balancer resources were deleted to avoid ongoing charges. The source code, Kubernetes manifests, Cloud Build configuration, documentation, screenshots, and container registry history remain as reproducible evidence of the implementation.
