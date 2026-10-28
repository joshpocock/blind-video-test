# blind-video-test

A Claude Code skill that runs a fair, blind test of AI video models: it plans
the rounds and writes one prompt per round that is fair to every model,
shuffles your downloaded clips into numbered blind copies, keeps the
scorecard, and reveals the results last place to first with totals, attempts,
credits and points per 100 credits.

Built from a test of nine video models on Higgsfield, four rounds, scored
blind. It works with any models on any platform.

It never generates anything and never spends credits. You make every clip;
Claude writes the prompts, shuffles, keeps the scores and runs the reveal,
and never peeks at which clip is which.

## What you get

- **A planner** that picks rounds with one known weak spot each (dialogue
  timing, fast motion, hands, the phone-footage look, a pour, a crowd ...) and
  writes one prompt per round, the same for every model.
- **Prompt rules** for a fair prompt: playback order, one camera move, real
  light from a fixed source, dialogue that gets said on time, what to leave
  out, and a pre-check that does not spoil the blind.
- **A shuffle** that gives each model one clip number for the whole test, so
  clip 4 is the same model in every round.
- **A five-mark scorecard**, 0 to 2 each, out of 10 per clip.
- **A reveal**, one model per Enter press, last place first, then the winner,
  the best value and each round's winner.
- **A worked example:** nine models, four rounds, the exact prompts.

## What it does

| You ask | Claude does |
|---|---|
| "Blind test these 5 video models on product shots." | Writes `rounds.md`: the lineup, the settings, the fairness rules, then one prompt per round (each a different hard case of product shots), its length and its hard part line. Writes `models.json` for your prices. |
| "Which video model is best for dialogue?" | Same, with every round a different dialogue weak spot: timing, two speakers, a line read off a sign. |
| "Write a fair prompt for every model: a man pouring coffee." | Writes one prompt to the rules (subject, action, camera, look, sound; one camera move; fixed light; each sound next to its event; under about 1,000 characters) and the hard part line. |
| "Shuffle the clips for round 2." | Runs `blind.py`: copies the round to `clip-1 ... clip-N` with the same numbers as round 1, writes an empty `scores.csv`, records reruns. Stops if a model is missing. |
| "Score this round: clip 1 is 2, 1, 2, 2, 1. Clip 2 is a 6." | Writes your numbers into that round's `scores.csv` and reads the row back. Never scores for you, never opens the key. |
| "Run the reveal." / "Who won?" | Runs `reveal.py`: totals, places last to first, ties shown as ties, attempts, credits, points per 100 credits, then the winner, best value and each round's winner. Writes `reveal.json`. |

## Install

Copy the skill folder into your Claude Code skills:

```
# for every project
cp -r skills/blind-video-test ~/.claude/skills/

# or for one project
cp -r skills/blind-video-test <your-project>/.claude/skills/
```

On Windows, copy `skills\blind-video-test` to `%USERPROFILE%\.claude\skills\`.

Requirements:

- Python 3.9 or newer
- Nothing else: standard library only, Windows, macOS and Linux

Claude picks the skill up when you say things like "blind test these video
models", "compare AI video models", "which video model is best", "write a fair
prompt for every model", "shuffle the clips", "score this round" or "run the
reveal".

## Quick start (60 seconds of your time, plus render time)

1. **Plan.** "Use blind-video-test to compare these models: <your list>.
   Four rounds." Claude writes `rounds.md` and `clips/models.json`. Put the
   credits your Generate button shows into `models.json`.
2. **Generate.** Paste each round's prompt into every model with the same
   settings. Do not watch anything. Download each clip into
   `clips/round-1/`, `clips/round-2/` ... named by model id:
   `01-model-a.mp4`, `02-model-b.mp4`. A rerun after an error is
   `01-model-a-attempt-2.mp4`.
3. **Shuffle.** "Shuffle round 1." (or `python blind.py clips 1`). Repeat per
   round.
4. **Score.** Open only `clips/round-1/blind/`. Watch each clip twice with
   sound and score it out of 10. Tell Claude the numbers or type them into
   `scores.csv`.
5. **Reveal.** `python reveal.py clips` in your own terminal and press Enter
   for each model.

## The fairness rules

The point of the test is that nothing but the model changes:

1. One prompt per round, word for word, never rewritten for a model.
2. The same duration, aspect, resolution and sound for every model. If a model
   lacks one, use its closest option and note it with the results, not in the
   prompt.
3. Text only: no reference images, no start frames, prompt-enhancer toggles
   off.
4. One take each. Rerun only on an error, and count it as an attempt.
5. Original people and fictional brands only. No text on screen.
6. Download without watching, shuffle, score by clip number, then reveal.

Before the real run, try each prompt on one cheap model that is **not** in
your lineup. It catches prompt problems (burned-in captions, a misread camera
move) without showing you any of the models you are about to judge.

## The scorecard

Five marks per clip, 0, 1 or 2 each, out of 10:

| Mark | 2 = nailed | 1 = partly | 0 = failed |
|---|---|---|---|
| Brief | everything the prompt asked for, in order | one or two things missing | most of it missing |
| The hard part | the round's own weak spot, all of it | one slip | it broke |
| Face and body | same face and body throughout, normal hands and limbs | one glitch | a face changes, limbs or fingers break |
| Sound | every sound matches its action, on time | one sound missing or late | no sound, or wrong sounds |
| Looks real | you'd scroll past it as real | AI in places | obviously AI |

Value is points per 100 credits: a model's total divided by what its clips
cost, times 100. The winner is often not the best value.

## The references

The skill reads these from `skills/blind-video-test/references/`:

| File | What is in it |
|---|---|
| `prompt-rules.md` | 20 rules for a prompt that is fair to every model, each with why, a template and a checklist |
| `scorecard.md` | the five marks, the hard part per round, how to score, value maths, ties |
| `round-ideas.md` | the four worked rounds with their prompts, ten more one-weak-spot rounds, and how to pick rounds for "best for X" |

## The scripts

Both have `--help`, take the clips folder as an argument, need no network and
no packages.

### blind.py

```
python blind.py <clips folder> <round> [--models models.json]
```

- The first run shuffles the lineup once and saves the key to
  `<clips folder>/.key.json`. Every round reuses it.
- The lineup is `models.json` (by default `<clips folder>/models.json`), or
  the first shuffled round's files if there is none. Use a `models.json`: it
  catches a model missing from round 1.
- Copies `round-N/<id>.mp4` to `round-N/blind/clip-K.mp4` with fresh file
  dates, writes `scores.csv` (clip, the five marks, total, notes) and
  `attempts.json` (from `-attempt-2`, `-attempt-3` file names; the highest
  attempt is the one scored).
- Stops, writing nothing, if a model is missing or a file is not in the
  lineup. Refuses a round that already has a `blind/` folder.

### reveal.py

```
python reveal.py <clips folder> [--models models.json] [--usd-per-credit X] [--json out.json] [--no-pause]
```

- Finds every `round-N` folder and adds each model's scores: out of 10 per
  round, out of 40 for four rounds.
- Takes the five marks or the total from `scores.csv`; if both are filled,
  they must agree. Stops on a missing score or a mark outside 0 to 2.
- Prints last place to first, one model per Enter press: model, clip number,
  per-round scores, total, attempts, credits a clip and for all its clips,
  points per 100 credits (and dollars with `--usd-per-credit`, your plan price
  divided by its credits). Equal totals share a place (`#3=`).
- Ends with the winner, the best value and each round's winner, and writes
  `reveal.json`.
- Credits count one clip per round. Reruns are listed, not charged, because
  platforms differ on refunds for failed generations.

### models.json

```
{
 "_note": "anything starting with _ is ignored",
 "01-model-a": {"name": "Model A", "credits": 20},
 "02-model-b": {"name": "Model B", "credits": null}
}
```

The ids are the file names. `null` credits means unknown: the model is still
ranked but left out of the value score. `scripts/models.example.json` holds
the nine-model lineup from the example, with the credits Higgsfield showed on
2026-10-22 to 2026-10-26 for a 10 s, 16:9, 1080p clip. Prices change; read
your Generate button.

## Example

`examples/nine-models-four-rounds/`: nine models on Higgsfield, four rounds
(dialogue, fast motion, hands, real or AI), 10 s, 16:9, 1080p, sound on.
`rounds.md` has the lineup, settings, fairness rules, the four prompts (887
to 1,006 characters) and each round's hard part. `models.json` is the lineup
with credits.

### How the scripts were tested

With dummy clips (any bytes) and filled-in scores:

| Test | Expected | Result |
|---|---|---|
| 9 models, 4 rounds, one `-attempt-2` in round 3 | same clip number per model in every round | every `clip-K` held the same model in rounds 1 to 4 |
| a clip missing in round 2 | stop, write nothing | stopped, named the missing model, no `blind/` folder written |
| shuffle round 1 again | refuse | refused, round 1 untouched |
| reveal, 9 models | totals out of 40, ties shared, value right | totals out of 40, two ties shown as `#3=` and `#1=`, 34/40 at 20 credits a clip = 42.5 points per 100 credits, the rerun shown as "5 attempts for 4 clips" |
| marks that do not add up to the total, a mark of 3, a half-filled row, an empty score | stop with the clip named | each one stopped with the file, clip and problem |
| 3 models, 2 rounds, custom `models.json`, one model with no price | totals out of 20, value only where priced | totals out of 20, a three-way tie for first, best value among the priced models only |

## Limits

- The scripts keep the test blind; they cannot keep you blind. Do not open
  `.key.json`, do not watch clips in the `round-N` folders, and do not compare
  file sizes between a round folder and its `blind/` copy.
- A model's look can give it away after a round or two. That is fine: score
  what is on screen, and never change an earlier round's scores.
- One take per model is a snapshot, not an average. A model can have a bad
  roll. Reruns only on errors keep it fair, not certain.
- Prices, settings and model names change. The example's credits were seen on
  2026-10-22 to 2026-10-26.

## License

MIT. Copyright (c) 2026 Josh Pocock.
