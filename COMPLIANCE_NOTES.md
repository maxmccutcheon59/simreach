# Compliance Notes — SimReach

> Human / lawyer review recommended before any commercial, classroom, or organizational deployment.
> This file flags legal and compliance-relevant aspects; it is **not** legal advice.

## Product posture

- **Sim-first educational robotics scaffold:** ROS 2 package layout + Gazebo world stub + unit-testable vision-guided approach logic.
- **No hardware purchases** required or authorized by this repo (see `BOM.md` research-only list; **$0** for v0.2.0).
- **No SaaS, accounts, telemetry, or intentional PII collection.**
- Recorded-run JSONL logs contain only synthetic geometry / twist numbers — no camera of people by default.
- Portfolio project for Max McCutcheon (`@maxmccutcheon59`).

## Data inventory

| Data | Collected by this repo? | Storage | Shared? |
|------|-------------------------|---------|---------|
| End-user PII | **No** | — | — |
| Camera frames (if operator runs ROS node) | Processed in-memory when subscribed | Not retained by default | Local ROS graph only |
| Recorded-run JSONL | Operator-chosen local file | Local disk if `-o` used | Not uploaded by this project |
| Telemetry / analytics | **None** | — | — |
| Payment / BOM purchases | **None** (do not buy for v0.2.0) | — | — |

## Privacy / regulatory flags

| Item | Applies? | Action |
|------|----------|--------|
| Privacy Policy / ToS | No (no user data service) | Re-review if productized |
| GDPR / US state privacy | No intentional PII | Operator responsibility if cameras capture people |
| COPPA / minors | No | Do not deploy as a child-directed product without review |
| Payments / PCI | No | BOM is research-only |
| HIPAA / health | No | N/A |
| Biometric / face data | **Not intended** | Color-blob marker only; do not train face models here |
| Export controls / sanctions | General-purpose robotics software | Human review if shipping to restricted jurisdictions |
| Workplace robot safety | Soft limits only | Future hardware: escalate for safety standards review (e.g. ISO 10218 / RIA references) — **not claimed compliant** |
| IP / third-party | MIT original code; ROS/Gazebo via their licenses in Docker | Do not vendor unlicensed meshes/textures |

## Camera / workplace ethics

- If a real camera is ever connected, the **operator** must ensure lawful recording (consent, workplace policy, no covert capture).
- This project does not provide surveillance features.

## Security tooling ethics

- Authorized systems only (see `SECURITY.md`).
- No exploit payloads, motor bypass, or safety-disable features.

## Items needing human review before commercial or lab use

- [ ] Lab / makerspace safety policy and physical e-stop before any powered arm
- [ ] Privacy Policy / Terms if a hosted multi-user product is built
- [ ] Export / sanctions screening if distributing binaries internationally
- [ ] Any ML model trained on images of people (out of scope; escalate)
