# Security Policy

ApplyTrack API is a portfolio project. This policy describes how secrets and test-only behavior are handled in the repository.

## Secrets and credentials

- Database credentials and other secrets are supplied through environment variables or cloud secret mechanisms (for example, Kubernetes Secrets in GKE).
- Do not commit `.env` files, service account keys, kubeconfig files, or database connection strings.
- `.env` is gitignored and intended for local development only.
- `.env.example` contains an obviously fake PostgreSQL URL shape and no real credentials.

## Test-only endpoints

- `GET /test-error` returns HTTP 500 only when `ENABLE_TEST_ENDPOINTS=true`.
- The setting defaults to `false`. When disabled, the route returns HTTP 404.
- Keep `ENABLE_TEST_ENDPOINTS` disabled in shared, staging, and cloud environments. Use it only for controlled local observability exercises.

## Reporting a vulnerability

If you believe you found a security issue in this repository, please open a private GitHub security advisory or contact the repository owner directly. Do not open a public issue for sensitive reports.

This project does not operate a production on-call security program or bug bounty.
