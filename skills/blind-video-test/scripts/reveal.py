#!/usr/bin/env python3
"""
reveal.py: unmask a blind video model test one model at a time, last place
to first.

Usage:
  python reveal.py <clips folder> [--models models.json] [--usd-per-credit 0.01]
                   [--json reveal.json] [--no-pause]

Finds every round-N folder in the clips folder, reads the one shuffle key
(<clips folder>/.key.json) and each round's blind/scores.csv and
blind/attempts.json, and adds up each model's scores (out of 10 per round).

Then it prints one model per Enter press, from the lowest total to the
highest: the model, the clip number it had, its score in each round, its
total, its attempts, credits a clip and for all its clips, and points per 100
credits. Ties are shown as ties. It ends with a summary (the winner, the best
value, each round's winner) and writes everything to reveal.json.

scores.csv: fill the five marks (brief, hard_part, face_and_body, sound,
looks_real, each 0 to 2) or just the total (0 to 10). If both are filled they
must agree.

Credits come from models.json ({"model-id": {"name": "...", "credits": 20}}),
by default <clips folder>/models.json. Without it, models are shown by id and
the value columns are left out.

--no-pause prints everything at once (use it when running from a script or an
assistant). --usd-per-credit adds dollars: your plan price divided by the
credits it includes.

Standard library only. Windows, macOS and Linux.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

PROG = "reveal.py"
MARKS = ["brief", "hard_part", "face_and_body", "sound", "looks_real"]
TOTAL_COLS = ["total", "total_out_of_10"]
ROUND_DIR = re.compile(r"^round-(\d+)$")


def die(msg: str) -> None:
    sys.stderr.write(f"{PROG}: {msg}\n")
    sys.exit(2)


def num(text: str, where: str, lo: float, hi: float) -> float:
    try:
        v = float(text)
    except ValueError:
        die(f"{where}: '{text}' is not a number.")
    if not lo <= v <= hi:
        die(f"{where}: {v:g} is outside {lo:g} to {hi:g}.")
    return v


def fmt(v: float) -> str:
    return f"{v:g}"


def load_models(path: Path) -> dict:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        die(f"{path} not found.")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON: {e}")
    if not isinstance(raw, dict):
        die(f"{path} must be an object: {{\"model-id\": {{\"name\": ..., \"credits\": ...}}}}.")
    models = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        if not isinstance(v, dict):
            die(f"{path}: \"{k}\" must be an object with \"name\" and \"credits\".")
        credits = v.get("credits")
        if credits is not None and (isinstance(credits, bool) or not isinstance(credits, (int, float))
                                    or credits <= 0):
            die(f"{path}: \"{k}\" credits must be a number above 0, or null if unknown.")
        models[k] = {"name": str(v.get("name") or k), "credits": credits}
    if not models:
        die(f"{path} lists no models.")
    return models


def load_round(round_dir: Path, key: dict) -> dict:
    """Return {model id: (score out of 10, attempts)} for one round."""
    blind = round_dir / "blind"
    if not blind.is_dir():
        die(f"{blind} is missing. Run blind.py for {round_dir.name} first, "
            "or move that folder out of the clips folder.")
    try:
        attempts = json.loads((blind / "attempts.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        attempts = {}
    scores_path = blind / "scores.csv"
    if not scores_path.exists():
        die(f"{scores_path} is missing.")
    scores = {}
    with open(scores_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        cols = {c.strip().lower(): c for c in (reader.fieldnames or [])}
        if "clip" not in cols:
            die(f"{scores_path} needs a 'clip' column.")
        mark_cols = [m for m in MARKS if m in cols]
        total_col = next((c for c in TOTAL_COLS if c in cols), None)
        for row in reader:
            clip = (row.get(cols["clip"]) or "").strip()
            if not clip:
                continue
            where = f"{scores_path} {clip}"
            marks = {m: (row.get(cols[m]) or "").strip() for m in mark_cols}
            filled = {m: v for m, v in marks.items() if v}
            total_txt = (row.get(cols[total_col]) or "").strip() if total_col else ""
            score = None
            if filled and len(filled) == len(MARKS):
                score = sum(num(v, f"{where} {m}", 0, 2) for m, v in filled.items())
                if total_txt and abs(num(total_txt, f"{where} total", 0, 10) - score) > 1e-9:
                    die(f"{where}: the marks add up to {fmt(score)} but total says {total_txt}. "
                        "Fix one of them.")
            elif total_txt:
                score = num(total_txt, f"{where} total", 0, 10)
            elif filled:
                left = [m for m in MARKS if m not in filled]
                die(f"{where} has only some marks. Still empty: {', '.join(left)}.")
            if score is None:
                die(f"{where} has no score yet.")
            if clip in scores:
                die(f"{scores_path} lists {clip} twice.")
            scores[clip] = score
    missing = [c for c in key if c not in scores]
    unknown = [c for c in scores if c not in key]
    if missing or unknown:
        die(f"{scores_path} does not match the shuffle. Missing: {missing or 'none'}. "
            f"Unknown: {unknown or 'none'}.")
    return {model: (scores[clip], int(attempts.get(model, 1))) for clip, model in key.items()}


def names(rows: list) -> str:
    ns = [r["model"] for r in rows]
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(
        prog=PROG,
        description="Reveal a blind video model test, last place to first.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example: python reveal.py clips --models models.json --usd-per-credit 0.01",
    )
    ap.add_argument("clips_folder", help="folder holding .key.json and round-1/, round-2/ ...")
    ap.add_argument("--models", help="models.json with names and credits "
                    "(default: <clips folder>/models.json if it exists)")
    ap.add_argument("--usd-per-credit", type=float,
                    help="your plan price divided by the credits it includes")
    ap.add_argument("--json", help="where to write the results (default: <clips folder>/reveal.json)")
    ap.add_argument("--no-pause", action="store_true",
                    help="print every row at once instead of one per Enter press")
    a = ap.parse_args()

    base = Path(a.clips_folder).expanduser()
    key_path = base / ".key.json"
    if not key_path.exists():
        die(f"{key_path} not found. Run blind.py on the first round before revealing.")
    key = json.loads(key_path.read_text(encoding="utf-8"))

    models_path = Path(a.models).expanduser() if a.models else base / "models.json"
    lineup = load_models(models_path) if (a.models or models_path.exists()) else None
    if lineup is not None:
        unknown = sorted(set(key.values()) - set(lineup))
        absent = sorted(set(lineup) - set(key.values()))
        if unknown or absent:
            die(f"The shuffle and {models_path.name} disagree. "
                f"Not in {models_path.name}: {unknown or 'none'}. "
                f"In {models_path.name} but never shuffled: {absent or 'none'}.")

    round_dirs = sorted(((int(m.group(1)), p) for p in base.iterdir()
                         if p.is_dir() and (m := ROUND_DIR.match(p.name))), key=lambda t: t[0])
    if not round_dirs:
        die(f"No round-N folders in {base}.")
    rounds = [(n, load_round(p, key)) for n, p in round_dirs]
    nums = [n for n, _ in rounds]
    out_of = 10 * len(rounds)
    clip_of = {model: clip for clip, model in key.items()}

    table = []
    for model in key.values():
        info = lineup[model] if lineup else {"name": model, "credits": None}
        per_round = [r[model][0] for _, r in rounds]
        attempts = [r[model][1] for _, r in rounds]
        total = sum(per_round)
        credits = info["credits"]
        credits_all = credits * len(rounds) if credits else None
        table.append({
            "model": info["name"], "id": model, "clip": clip_of[model],
            "rounds": {str(n): s for n, s in zip(nums, per_round)},
            "attempts": {str(n): t for n, t in zip(nums, attempts)},
            "total": total, "out_of": out_of,
            "credits_per_clip": credits, "credits_all_clips": credits_all,
            "points_per_100_credits": round(total / credits_all * 100, 1) if credits_all else None,
            "usd_all_clips": round(credits_all * a.usd_per_credit, 2)
            if credits_all and a.usd_per_credit else None,
        })
    for row in table:
        row["place"] = 1 + sum(1 for r in table if r["total"] > row["total"])
        row["tied_with"] = [r["model"] for r in table if r is not row and r["total"] == row["total"]]
    clip_no = lambda r: int(r["clip"].split("-")[-1]) if r["clip"].split("-")[-1].isdigit() else 0
    table.sort(key=lambda r: (r["total"], -clip_no(r)))  # lowest first; ties by clip number

    pause = not a.no_pause
    print(f"\nTHE REVEAL: {len(table)} models, {len(rounds)} round"
          f"{'' if len(rounds) == 1 else 's'}, out of {out_of}.")
    if pause:
        print("Press Enter for each model, last place first.")
    print()
    for row in table:
        if pause:
            try:
                input()
            except EOFError:
                pause = False
        place = f"#{row['place']}{'=' if row['tied_with'] else ''}"
        scores = " / ".join(fmt(s) for s in row["rounds"].values())
        print(f"{place}  {row['model']}  {fmt(row['total'])}/{out_of}  (rounds: {scores})")
        if row["tied_with"]:
            print(f"     tied with {', '.join(row['tied_with'])}")
        tries = sum(row["attempts"].values())
        n_clips = len(rounds)
        if tries == n_clips:
            tries_note = "one take each"
        else:
            reruns = [f"round {n}: {t}" for n, t in row["attempts"].items() if t > 1]
            tries_note = f"{tries} attempts for {n_clips} clips ({', '.join(reruns)})"
        print(f"     was {row['clip']}, {tries_note}")
        if row["credits_per_clip"]:
            money = f", about ${row['usd_all_clips']:.2f}" if row["usd_all_clips"] is not None else ""
            span = "one clip" if n_clips == 1 else ("both clips" if n_clips == 2 else f"all {n_clips} clips")
            print(f"     {fmt(row['credits_per_clip'])} credits a clip, "
                  f"{fmt(row['credits_all_clips'])} for {span}{money}, "
                  f"{row['points_per_100_credits']:g} points per 100 credits")
        elif lineup is not None:
            print("     no credits in models.json, so no value score")
        print()

    ranked = list(reversed(table))
    top = [r for r in ranked if r["place"] == 1]
    priced = [r for r in ranked if r["points_per_100_credits"] is not None]
    summary = {"winner": [r["model"] for r in top], "winner_total": top[0]["total"],
               "out_of": out_of, "best_value": [], "round_winners": {}}
    print("SUMMARY")
    label = "Winner" if len(top) == 1 else "Joint winners"
    print(f"  {label}: {names(top)}, {fmt(top[0]['total'])}/{out_of}")
    if priced:
        ratio = lambda r: r["total"] / r["credits_all_clips"]  # unrounded, so rounding makes no false ties
        best_ratio = max(ratio(r) for r in priced)
        value = [r for r in priced if abs(ratio(r) - best_ratio) < 1e-12]
        best = value[0]["points_per_100_credits"]
        summary["best_value"] = [r["model"] for r in value]
        summary["best_value_points_per_100_credits"] = best
        detail = "; ".join(f"{r['model']} {fmt(r['total'])}/{out_of} for "
                           f"{fmt(r['credits_all_clips'])} credits" for r in value)
        print(f"  Best value: {names(value)}, {best:g} points per 100 credits ({detail})")
        if len(priced) < len(table):
            print("  (Best value leaves out models with no credits in models.json.)")
    else:
        print("  Best value: needs credits in models.json.")
    for n in nums:
        hi = max(r["rounds"][str(n)] for r in table)
        winners = [r for r in ranked if r["rounds"][str(n)] == hi]
        summary["round_winners"][str(n)] = {"models": [r["model"] for r in winners], "score": hi}
        tie = ", tie" if len(winners) > 1 else ""
        print(f"  Round {n}: {names(winners)} ({fmt(hi)}/10{tie})")

    out_path = Path(a.json).expanduser() if a.json else base / "reveal.json"
    out_path.write_text(json.dumps({"rounds": nums, "out_of": out_of, "table": ranked,
                                    "summary": summary}, indent=1), encoding="utf-8")
    print(f"\nSaved {out_path}")


if __name__ == "__main__":
    main()
