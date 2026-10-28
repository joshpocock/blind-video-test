---
name: blind-video-test
description: Run a fair, blind test of AI video models. Plans the rounds (one known weak spot per round, one identical text prompt for every model, the same settings, one take each), shuffles the downloaded clips into numbered blind copies with the same clip number for a model in every round, keeps a five-mark scorecard out of 10 per clip, and reveals the results last place to first with totals, attempts, credits and points per 100 credits. Works with any set of models on any platform. Use when the user says "blind test these video models", "compare AI video models", "which video model is best", "which video model is best for dialogue", "test these models on product shots", "write a fair prompt for every model", "plan the rounds", "shuffle the clips", "score this round", "log my scores", "run the reveal" or "who won".
---

# Blind Video Test

You help the user find out which AI video model is best for a kind of shot, fairly. Every model gets the same prompt and settings, the user scores the clips without knowing which model made them, and the names and prices come out only at the end.

Four modes:

1. **PLAN**: pick or write the rounds, one prompt per round, the settings, and the hard part each round is scored on.
2. **SHUFFLE**: turn each round's downloaded clips into `clip-1 ... clip-N` with `blind.py`.
3. **SCORE**: the user scores each clip on five marks, 0 to 2 each, out of 10. You record the numbers.
4. **REVEAL**: `reveal.py` adds it up and unmasks the models last place to first.

## Ground rules

- **You never generate.** The user makes every clip on their platform. Do not call any video generation tool or API from this skill and never spend the user's credits.
- **Never break the blind.** Do not open, read, print or summarise `.key.json`. Do not compare file sizes, dates or contents between `round-N/` and `round-N/blind/`. Do not say which model a clip is, or guess, before the user runs the reveal. If the user asks, say the reveal will tell them, and that opening the key now spoils every round still to score.
- **Never quote prices as current.** Credits in `models.json` are what the user read on the Generate button. Prices and promos change; tell them to check before every run.
- **The human scores.** You can take notes and fill `scores.csv` with numbers the user gives you. You do not score clips yourself.
- **Original people and fictional brands only.** No real people, celebrities, known characters, real products or real logos in any prompt.
- Which reference to read when:

  | Reference | Read it in | For |
  |---|---|---|
  | `references/prompt-rules.md` | PLAN | writing a prompt that is fair to every model |
  | `references/round-ideas.md` | PLAN | the four worked rounds and more one-weak-spot ideas |
  | `references/scorecard.md` | PLAN (the hard part line), SCORE, REVEAL | the five marks, what 2, 1 and 0 mean, value maths |

## Setup (once)

```
python --version     # 3.9 or newer, standard library only
```

The scripts live in `scripts/` next to this file. Run them with full paths and pass the user's clips folder as an argument. Both have `--help`.

Suggested test folder:

```
my-test/
  rounds.md                 the prompts, settings and hard parts (you write it in PLAN)
  clips/
    models.json             the lineup: id -> {"name", "credits"}
    round-1/                01-model-a.mp4  02-model-b.mp4 ...
      blind/                clip-1.mp4 ... scores.csv  attempts.json  (blind.py writes it)
    round-2/ ...
    .key.json               the shuffle (blind.py writes it; nobody opens it)
    reveal.json             (reveal.py writes it)
```

---

## Mode 1: PLAN

Input: what the user wants to compare, for example "test these 5 models on product shots" or "which video model is best for dialogue". If something essential is missing (which models, what kind of shot), pick a sensible default and say so. Ask at most one question.

1. **The lineup.** List the models with an id each (`01-model-name`, lower case, hyphens) and write `clips/models.json` from `scripts/models.example.json`. Ask the user to read each price on the Generate button at the test settings and put it in `credits`, or `null` if unknown.
2. **The rounds.** Default 4, at least 2. Each round tests **one known weak spot** that anyone can judge in ten seconds (dialogue timing, fast motion, hands, the phone-footage look, a pour, a crowd). Start from `references/round-ideas.md`; for "best for X", make every round a different hard case of X.
3. **One prompt per round.** Write it with `references/prompt-rules.md`: subject, action, camera, look, sound, in that order, under about 1,000 characters, ending "No music, no subtitles, no text on screen." Count the characters and report them.
4. **The hard part line** for each round: one sentence that says what a 2 looks like on that round's weak spot. It goes in the scorecard.
5. **Settings.** One duration, aspect ratio, resolution and sound setting for every model: the longest duration every model can do, then the most common aspect and resolution. If a model lacks one, use its closest option and note it for the results (on screen or in the write-up), not in the prompt.
6. **The fairness rules**, written at the top of `rounds.md` so the user sees them on the day:
   - One prompt per round, word for word, never rewritten for a model.
   - Same duration, aspect, resolution and sound for all (closest option if a model lacks one, noted).
   - Text only: no reference images, no start frames, prompt-enhancer or "magic prompt" toggles off.
   - One take each. Rerun only on an error, and the rerun counts as an attempt (`-attempt-2`).
   - Original people and fictional brands only. No text on screen.
   - Download without watching.
7. **Pre-check.** Before the real run, suggest running each prompt once on one cheap model that is **not** in the lineup. It catches prompt-level problems (burned-in captions, a misread camera move, a line nobody can say, a clip that comes back the wrong shape) without spoiling the blind. Fix the prompt, never per model.

Write `rounds.md`: the lineup, the settings, the fairness rules, then per round its name, the weak spot, the prompt in a code block, its length and the hard part line. `examples/nine-models-four-rounds/` in the repository is a finished one.

Close with the run sheet: pre-check, generate every round on every model without watching, download into `clips/round-N/`, shuffle each round, score, reveal.

---

## Mode 2: SHUFFLE

The user downloads every clip of a round without watching it, into `clips/round-N/`, named by model id: `01-model-a.mp4`, `02-model-b.mp4` ... The id must be the same in every round and match `models.json`. A rerun after an error is `01-model-a-attempt-2.mp4`; the highest attempt is the clip that gets scored.

```
python <skill>/scripts/blind.py clips 1
python <skill>/scripts/blind.py clips 2
```

(`--models path/to/models.json` when it is not in the clips folder.)

What it does:

- The first run shuffles the lineup once and saves the key to `clips/.key.json`. Every later round reuses it, so clip 4 is the same model in every round and the board builds across rounds.
- Copies the round's clips to `round-N/blind/clip-1.mp4 ... clip-N.mp4` (fresh file dates, so dates give nothing away), writes an empty `scores.csv` and records attempts in `attempts.json`.
- Stops without writing anything if a model is missing or a file is not in the lineup. Refuses to run on a round that already has a `blind/` folder.

Relay its message. If it stops, tell the user which file to fix; never "fix" it by renaming clips yourself unless the user asks, and then only by the name they give.

Tell the user: watch only the `blind/` folder, sorted by name, and do not compare file sizes with the round folder.

---

## Mode 3: SCORE

Read `references/scorecard.md`. Five marks per clip, each 0, 1 or 2, out of 10:

| Mark | 2 = nailed | 1 = partly | 0 = failed |
|---|---|---|---|
| Brief | everything the prompt asked for, in order | one or two things missing | most of it missing |
| The hard part | this round's hard part line | one slip | it broke |
| Face and body | same face and body throughout, normal hands and limbs | one glitch | a face changes, limbs or fingers break |
| Sound | every sound matches its action, on time | one sound missing or late | no sound, or wrong sounds |
| Looks real | you'd scroll past it as real | AI in places | obviously AI |

Score by clip number only. Watch each clip full screen with sound, at least twice, then score before the next one. Finish a round before moving on, and do not change a round's scores after you have seen later rounds.

When the user tells you scores ("clip 3: 2, 1, 2, 2, 1" or "clip 3 is a 7"), write them into `clips/round-N/blind/scores.csv`: columns `brief, hard_part, face_and_body, sound, looks_real`, or just `total`, plus `notes` in the user's words. Read back the row you wrote. Reading and writing `scores.csv` is fine; it holds clip numbers only.

---

## Mode 4: REVEAL

When every round is scored:

```
python <skill>/scripts/reveal.py clips --usd-per-credit 0.01
```

Options: `--models path.json` (default `clips/models.json`), `--usd-per-credit X` (plan price divided by credits included), `--json out.json` (default `clips/reveal.json`), `--no-pause`.

The Enter-press reveal is for the user's own terminal (it makes a good on-camera moment). When you run it, always pass `--no-pause`, and only after the user asks to see the results.

It finds every `round-N` folder, adds each model's scores (out of 10 per round), and prints last place to first, one model per Enter press: the model, the clip number it had, its score per round, its total, its attempts, credits a clip and for all its clips, and points per 100 credits. Ties are shown as ties (`#3=`). Then a summary: the winner, the best value (most points per 100 credits) and each round's winner. It stops if a score is missing, if the five marks and the total disagree, or if a mark is outside 0 to 2.

Then tell the user, in plain words: who won and by how much, the best value and why, which model won each weak spot, and anything the attempts column says (a model that needed reruns). Note that credits count one clip per round; errored attempts are listed but not charged, because platforms differ on refunds.

If they want to share it, offer a results table: model, each round, total, credits a clip, points per 100 credits, attempts, plus the settings and any closest-option notes.
