![CI - Lint YML](https://github.com/Daegybyte/kometa_yamls/actions/workflows/lint.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/lint.yml)
[![CI - Ruff](https://github.com/Daegybyte/kometa_yamls/actions/workflows/ruff.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/ruff.yml)
[![CI - Security](https://github.com/Daegybyte/kometa_yamls/actions/workflows/security.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/security.yml)
[![CI - Pytest](https://github.com/Daegybyte/kometa_yamls/actions/workflows/test.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/test.yml)
[![CD - Sync configs to plex](https://github.com/Daegybyte/kometa_yamls/actions/workflows/deploy.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/deploy.yml)
[![CD - Sync configs to plex-remote](https://github.com/Daegybyte/kometa_yamls/actions/workflows/deploy-plex-remote.yml/badge.svg)](https://github.com/Daegybyte/kometa_yamls/actions/workflows/deploy-plex-remote.yml)

# config-repo

YAML configuration repository with automated validation and multi-server synchronization using
GitHub Actions.

## Overview

This repository keeps configuration in source control and automatically distributes updates to
multiple Linux servers in a repeatable, deterministic way.

## (GitHub Actions)

## CI: YAML Linting

- A CI workflow runs on every push and pull request.
- It uses `yamllint` to catch common YAML issues early (rules are tuned for config-heavy YAML to
  avoid unnecessary reformatting).

## CI: Ruff

- Lints all Python helper scripts using Ruff, a fast Python linter written in Rust.
- Catches unused imports, style issues, and common bugs.

## CI: Security

- Scans Python helper scripts using Bandit.
- Checks for common vulnerabilities such as hardcoded credentials and shell injection risks.

## CI: Pytest & Coverage

- Runs the full test suite against all Python helper scripts using pytest.
- Enforces a minimum code coverage threshold of 99% against the `helpers/` directory.

## CD: Multi-Server Sync (Self-Hosted Runners)

- Separate CD workflows run on pushes to `main` to sync updates to multiple servers.
- Each server runs a **self-hosted GitHub Actions runner** as a **systemd service**, so deployments
  work without opening inbound firewall ports (the runner connects outbound to GitHub and waits for
  jobs).
- Deployments are **deterministic** and **idempotent**: the workflow performs `git fetch` +
  `git reset --hard origin/<default-branch>` so the server checkout matches the repo exactly.

### Runner Routing / Labels

With multiple self-hosted runners, workflows target the correct server using labels. Example
pattern:

- `runs-on: [self-hosted, $SERVER-NAME]` → deploys to the runner installed on `$SERVER-NAME`
- `runs-on: [self-hosted, $SERVER-NAME-REMOTE]` → deploys to the runner installed on
  `$SERVER-NAME-REMOTE`

Each server syncs its own working copy (e.g., `/home/$USERNAME/<repo-dir>`), which keeps deployments
predictable and prevents jobs from landing on the wrong host.

## Notes

- CI and CD are intentionally kept separate to mirror common real-world pipeline organization
  (validation vs. deployment).
- Label-based runner selection is required for multi-server environments; without unique labels,
  jobs may queue indefinitely or route to the wrong host.
