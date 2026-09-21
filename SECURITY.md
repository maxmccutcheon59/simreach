# Security Policy

## Supported versions

Security fixes are applied on the latest release of **SimReach** on `main`. Older tags are not backported unless noted in a release.

## Reporting a vulnerability

Please report security issues privately — do **not** open a public GitHub issue for undisclosed vulnerabilities.

- **Contact:** [MaxMcCutcheon1@outlook.com](mailto:MaxMcCutcheon1@outlook.com)
- Include: affected version/commit, reproduction steps, impact, and any suggested fix.
- You should receive an acknowledgment within a few business days.

We will work with you to understand and remediate the issue, then credit reporters who want acknowledgment (optional).

## Authorized testing only

SimReach is an **educational / portfolio robotics simulation** scaffold. You may only run it against systems **you own** or for which you have **explicit written authorization**.

Unauthorized scanning, access, or testing of third-party systems may violate the Computer Fraud and Abuse Act (CFAA), similar laws, and site Terms of Service.

- Intended use: local unit tests, Dockerized ROS 2 / Gazebo on your own machine, and future hardware **you own**.
- Do not point cameras at people without consent; do not deploy manipulators where they can injure people or damage property.

## Robot / sim safety (software)

- Soft Cartesian speed clamps and lost-target e-stop are **research aids**, not certified functional safety.
- Future hardware requires a **physical e-stop** and human safety review before power-on (see `BOM.md`).
- Containers run as a non-root user; do not bake secrets into images.

## Secrets and credentials

- Never commit secrets (`.env`, API keys, tokens, private keys).
- Use environment variables or a secrets manager for any credentials.
- If a secret is exposed: **rotate it first**, then clean history if needed.

## Preferred disclosure process

1. Email the contact above with details.
2. Allow reasonable time for a fix before public disclosure.
3. Coordinated disclosure is appreciated; please do not weaponize findings.

## Incident response (baseline)

1. Contain (disable network publish, power down hardware if any).
2. Rotate any exposed credentials.
3. Assess impact and notify affected parties if personal data were involved (none collected by default).
4. Patch, tag a fixed release, and document in `CHANGELOG.md`.
