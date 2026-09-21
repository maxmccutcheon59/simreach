"""Smoke-test the pure-Python recorded-run helper (no Gazebo)."""

from __future__ import annotations

import json
from pathlib import Path

from simreach_vision.recorded_run import run_recorded_sequence


def test_recorded_run_produces_rows(tmp_path: Path):
    out = tmp_path / "run.jsonl"
    rows = run_recorded_sequence(output_path=out, width=160, height=120)
    assert len(rows) >= 5
    assert out.is_file()
    lines = out.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(rows)
    first = json.loads(lines[0])
    assert "frame" in first and "reason" in first and "vx" in first
    reasons = {r["reason"] for r in rows}
    assert "align" in reasons or "approach" in reasons


def test_recorded_run_lost_tail_estop(tmp_path: Path):
    rows = run_recorded_sequence(
        output_path=tmp_path / "lost.jsonl",
        waypoints=[(80, 60), (80, 60)],
        width=160,
        height=120,
        lost_tail=6,
    )
    assert any(r["reason"] == "lost_target_estop" for r in rows)
