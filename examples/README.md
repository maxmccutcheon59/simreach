# Examples

- `sample_run.jsonl` — checked-in sample from `simreach_vision.recorded_run` (320×240).
- Generate a fresh log locally (gitignored if named `last_run.jsonl`):

```bash
python scripts/recorded_run.py -o examples/last_run.jsonl --lost-tail 6
```
