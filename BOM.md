# Bill of Materials — Future cheap arm (RESEARCH ONLY)

> **DO NOT BUY for SimReach v0.2.0 ($0 hardware).**  
> This file is a planning reference for a later milestone. No purchases are authorized or required by this repository. Prices are approximate public street prices (USD, 2026 research) and will change — verify before any future purchase decision by a human owner.

## Goal (future)

A low-cost, tabletop 4–6 DOF arm + wrist camera suitable for repeating the **sim** vision-guided approach on hardware **you own**, with clear soft/hard safety limits. Prefer kits with:

- Published kinematics / ROS 2 packages
- 5 V / 12 V benchtop power (no mains motor drives without review)
- E-stop or power cut that a human can reach

## Candidate research list (not an order form)

| Item | Role | Example class (illustrative) | Approx. USD | Notes |
|------|------|------------------------------|------------|-------|
| Desktop arm kit | Manipulator | Hobby 4–6 DOF servo arm (e.g. DIY kits in the ~$100–250 class) | 100–250 | Prefer open kinematics; avoid “toy only” with sealed firmware if you need ROS |
| USB camera | Eye-in-hand or scene | UVC 1080p webcam | 20–40 | Match `rgb8` pipeline; mount rigidly |
| SBC / NUC-class | Onboard compute | Existing laptop first; else used NUC / Pi-class | 0–200 | **Reuse hardware you already own** before buying |
| 5–12 V PSU | Arm power | Matched to kit spec with headroom | 15–40 | Correct polarity/current; fused |
| E-stop button | Human safety | NC mushroom switch in series with motor power | 10–25 | Hard power interrupt — software e-stop is not enough on hardware |
| Wiring / mounts | Integration | Breadboard-quality only for bring-up | 10–30 | Strain relief; no dangling power leads |
| Optional depth cam | Later perception | Not required for color-blob approach | 50–200+ | Defer |

**Rough future total if starting from zero:** ~$150–500. **Recommended v0.2.0 path:** $0 — simulation, unit tests, and `scripts/recorded_run.py` only.

## Explicit non-goals

- Industrial cobots, pneumatic grippers, or anything requiring facility power/permits
- Weapons, drones with payload, or outdoor autonomy
- Buying “because the README listed it”

## When hardware is reconsidered

1. Sim approach demos reliably (recorded-run and/or Gazebo/Docker).
2. Human writes a hardware safety checklist (e-stop, workspace fencing, torque limits).
3. Budget and shipping address confirmed by Max — not by an agent.
4. Update this BOM with exact SKUs, dates, and receipts in a private note (do not commit payment data).
