# Security

## Scope

Comment Synthesizer is a research and software-engineering prototype. The included FastAPI service is intended for local demonstration and development.

## Deployment guidance

Do not expose the demonstration API directly to the public internet without production controls appropriate to the deployment, including authentication and authorisation where required, rate limiting, restricted CORS, TLS termination, logging controls, dependency maintenance and input/request-size limits.

The project does not require API keys or credentials for its core rule-based response engine. Do not commit credentials, private datasets, customer messages or other sensitive information to this repository.

## Reporting a vulnerability

If you identify a security issue, please avoid publishing exploitable details in a public issue until the maintainer has had an opportunity to assess it. Use the repository owner's available private contact channel where possible.

## Data

The public repository does not intentionally include the historical research datasets referenced by scripts under `research/`. Those scripts are retained as research provenance only.
