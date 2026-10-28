#!/usr/bin/env python3
"""
blind.py: copy one round of AI video clips into numbered blind copies, with
the SAME clip number for a model in every round.

Usage (once per round, after the clips are downloaded and before you watch any):
  python blind.py <clips folder> <round number> [--models models.json]
  python blind.py clips 1
  python blind.py clips 2 --models models.json

The clips folder holds round-1/, round-2/ ... round-N/. Each round folder
holds one clip per model, named after the model: 01-minimax-h3.mp4,
02-kling-3-0.mp4 ... The file name without its extension is the model's id,
so it must be identical in every round (and match models.json if you use one).

Reruns: if a generation errored and you ran it again, name the new file
"<id>-attempt-2.mp4" (then "-attempt-3"). The highest attempt is the clip that
gets scored, and the attempt count is kept for the reveal.

The first run shuffles the models once and saves the answer key to
<clips folder>/.key.json. Do not open it. Every later round reuses that key,
so clip 4 is the same model in every round. Each run copies the clips into
<round>/blind/ as clip-1.mp4 ... clip-N.mp4, writes an empty scores.csv to
fill in while you score, and records attempts in attempts.json.

It stops, without writing anything, if a model is missing from the round or a
file is not in the lineup, and it refuses to touch a round that already has a
blind folder, so a reveal can never change by accident.

The lineup is models.json when given (or <clips folder>/models.json when it
exists), otherwise the files in the first round you shuffle. models.json maps
each id to {"name": "...", "credits": 20}; keys starting with "_" are notes.

Standard library only. Windows, macOS and Linux.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import re
import shutil
import sys
from pathlib import Path

PROG = "blind.py"
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm"}
ATTEMPT = re.compile(r"^(?P<model>.+?)-attempt-(?P<n>\d+)$")
MARKS = ["brief", "hard_part", "face_and_body", "sound", "looks_real"]
SCORE_HEADER = ["clip"] + MARKS + ["total", "notes"]


def die(msg: str) -> None:
    sys.stderr.write(f"{PROG}: {msg}\n")
    sys.exit(2)


def load_models(path: Path) -> dict:
    """Return {model id: {"name": str, "credits": number or None}} from models.json."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"{path} not found.")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON: {e}")
    if not isinstance(raw, dict):
        die(f"{path} must be an object: {{\"model-id\": {{\"name\": ..., \"credits\": ...}}}}.")
    models = {k: v for k, v in raw.items() if not k.startswith("_")}
    if not models:
        die(f"{path} lists no models.")
    for k, v in models.items():
        if not isinstance(v, dict):
            die(f"{path}: \"{k}\" must be an object with \"name\" and \"credits\".")
    return models


def parse_round(text: str) -> int:
    t = text.strip().lower()
    if t.startswith("round-"):
        t = t[len("round-"):]
    if not t.isdigit() or int(t) < 1:
        die(f"round must be a whole number from 1 up (got '{text}').")
    return int(t)


def find_clips(round_dir: Path) -> dict:
    """Return {model id: (scored file, attempts)} for every clip in a round folder."""
    found: dict = {}
    for p in sorted(round_dir.iterdir()):
        if not p.is_file() or p.suffix.lower() not in VIDEO_EXT:
            continue
        m = ATTEMPT.match(p.stem)
        model, n = (m["model"], int(m["n"])) if m else (p.stem, 1)
        found.setdefault(model, {})
        if n in found[model]:
            die(f"{round_dir}: two files for {model} attempt {n} "
                f"({found[model][n].name} and {p.name}). Keep one.")
        found[model][n] = p
    return {model: (files[max(files)], max(files)) for model, files in found.items()}


def main() -> None:
    ap = argparse.ArgumentParser(
        prog=PROG,
        description="Shuffle one round of clips into blind copies (clip-1 ... clip-N). "
                    "One shuffle, reused every round.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python blind.py clips 1 --models models.json",
    )
    ap.add_argument("clips_folder", help="folder holding round-1/, round-2/ ...")
    ap.add_argument("round", help="round number (1, 2, 3 ...)")
    ap.add_argument("--models", help="models.json with the lineup "
                    "(default: <clips folder>/models.json if it exists)")
    a = ap.parse_args()

    base = Path(a.clips_folder).expanduser()
    if not base.is_dir():
        die(f"{base} is not a folder.")
    n = parse_round(a.round)
    round_dir = base / f"round-{n}"
    if not round_dir.is_dir():
        die(f"{round_dir} does not exist. Put round {n}'s clips in it first.")

    out = round_dir / "blind"
    if out.exists():
        die(f"{out} already exists. Round {n} is already shuffled. "
            "Delete that folder yourself only if you really mean to redo the round.")

    models_path = Path(a.models).expanduser() if a.models else base / "models.json"
    lineup = load_models(models_path) if (a.models or models_path.exists()) else None

    clips = find_clips(round_dir)
    if not clips:
        die(f"No video files in {round_dir} (looked for {', '.join(sorted(VIDEO_EXT))}).")

    key_path = base / ".key.json"
    key = None
    if key_path.exists():
        try:
            key = json.loads(key_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            die(f"{key_path} is damaged. Do not edit it by hand.")
        expected = set(key.values())
        if lineup is not None and set(lineup) != expected:
            die(f"{models_path.name} no longer matches the shuffle in {key_path.name}. "
                f"In models.json only: {sorted(set(lineup) - expected) or 'none'}. "
                f"In the shuffle only: {sorted(expected - set(lineup)) or 'none'}. "
                "Put models.json back the way it was when you shuffled round 1.")
        where = "the shuffle (.key.json)"
    elif lineup is not None:
        expected = set(lineup)
        where = models_path.name
    else:
        expected = set(clips)
        where = "this round's files"

    missing = sorted(expected - set(clips))
    extra = sorted(set(clips) - expected)
    if missing or extra:
        msg = (f"{round_dir} does not match {where}. "
               f"Missing: {missing or 'none'}. Not in the lineup: {extra or 'none'}. "
               "Fix the file names (or download the missing clip) and run again. Nothing was written.")
        if key is not None and lineup is None and extra:
            msg += (" The shuffle was made from round files without a models.json; if round 1 "
                    "was missing a model, delete .key.json and every round's blind folder, "
                    "add a models.json and start again.")
        die(msg)

    if key is None:
        order = sorted(expected)
        random.SystemRandom().shuffle(order)
        key = {f"clip-{i}": model for i, model in enumerate(order, start=1)}
        key_path.write_text(json.dumps(key, indent=1), encoding="utf-8")
        print(f"New shuffle of {len(key)} models saved to {key_path}. "
              "Every round uses it. Do not open it.")

    out.mkdir()
    attempts = {}
    for clip, model in key.items():
        src, tries = clips[model]
        # copyfile, not copy2: the copies get fresh dates, so dates cannot hint at the model.
        shutil.copyfile(src, out / f"{clip}{src.suffix.lower()}")
        attempts[model] = tries
    (out / "attempts.json").write_text(json.dumps(attempts, indent=1, sort_keys=True),
                                       encoding="utf-8")
    with open(out / "scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(SCORE_HEADER)
        for clip in key:
            w.writerow([clip] + [""] * (len(SCORE_HEADER) - 1))

    reruns = sum(1 for t in attempts.values() if t > 1)
    print(f"Round {n}: {len(key)} clips copied to {out} as clip-1 to clip-{len(key)} "
          f"({reruns} rerun{'' if reruns == 1 else 's'}).")
    print(f"Score them by number in {out / 'scores.csv'} "
          "(five marks 0, 1 or 2, or just the total out of 10). Watch only the blind folder.")


if __name__ == "__main__":
    main()
