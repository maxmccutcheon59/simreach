#!/usr/bin/env python3
"""
Example recorded approach run — pure Python, no Gazebo.

Usage (from repo root, after ``pip install -e ".[dev]"``)::

    python scripts/recorded_run.py
    python scripts/recorded_run.py --output examples/last_run.jsonl --lost-tail 6

Writes a JSONL log of detections and twist commands for portfolio demos / CI.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))

from simreach_vision.recorded_run import default_waypoints, run_recorded_sequence  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="SimReach pure-Python recorded approach run")
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="JSONL output path (default: print summary only)",
    )
    p.add_argument("--width", type=int, default=640)
    p.add_argument("--height", type=int, default=480)
    p.add_argument("--radius", type=int, default=10)
    p.add_argument(
        "--lost-tail",
        type=int,
        default=0,
        help="Blank frames after waypoints to demo lost-target hold/e-stop",
    )
    p.add_argument("--quiet", action="store_true", help="Suppress per-frame stdout")
    args = p.parse_args(argv)

    if args.width <= 0 or args.height <= 0:
        print("width and height must be positive", file=sys.stderr)
        return 2

    rows = run_recorded_sequence(
        output_path=args.output,
        waypoints=default_waypoints(args.width, args.height),
        width=args.width,
        height=args.height,
        radius=args.radius,
        lost_tail=max(0, args.lost_tail),
    )

    if not args.quiet:
        for row in rows:
            print(
                f"frame={row['frame']:02d} found={row['found']} "
                f"u={row['det_u']:.1f} v={row['det_v']:.1f} "
                f"vx={row['vx']:.4f} vy={row['vy']:.4f} vz={row['vz']:.4f} "
                f"reason={row['reason']} estop={row['estop']}"
            )
        summary = {
            "frames": len(rows),
            "reasons": sorted({r["reason"] for r in rows}),
            "estop_frames": sum(1 for r in rows if r["estop"]),
            "output": str(args.output) if args.output else None,
        }
        print("---")
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
