# The scorecard

Five marks per clip, each 0, 1 or 2. Total out of 10 per clip, so a model's
total is out of 10 times the number of rounds (40 for four rounds).

The same five marks every round. Only "the hard part" changes, and it is the
weak spot the round is named for.

## The five marks

| Mark | 2 = nailed | 1 = partly | 0 = failed |
|---|---|---|---|
| Brief | everything the prompt asked for, in order | one or two things missing | most of it missing |
| The hard part | the round's hard part line, all of it | one slip | it broke |
| Face and body | same face and body throughout, normal hands and limbs | one glitch | a face changes, limbs or fingers break |
| Sound | every sound matches its action, on time | one sound missing or late | no sound, or wrong sounds |
| Looks real | you'd scroll past it as real | AI in places | obviously AI |

Notes on each:

- **Brief.** Go through the prompt in order. Count what is missing or out of
  order. A cut when the prompt said "no cuts", music when it said "no music"
  and burned-in captions are all brief misses.
- **The hard part.** Judge only the round's weak spot here, against its line
  (below). Do not take points off twice: a broken hand in the hands round costs
  the hard part, not also face and body, unless something else breaks too.
- **Face and body.** Watch the face across the whole clip, then the hands and
  limbs. Count fingers when hands are close. For an animal, the body: legs,
  tail, head. A subject seen only from behind is judged on body alone.
- **Sound.** With sound on. Every sound in the prompt, at the moment its event
  happens. A spoken line counts here for being there and on time; the exact
  words count under the hard part in a dialogue round, or under brief.
- **Looks real.** Your gut, after the second watch. Would you believe it if it
  came up in your feed?

## The hard part, per round

Write one line per round in PLAN: what a 2 looks like on that round's weak
spot. The four example rounds:

| Round | 2 = nailed |
|---|---|
| 1, dialogue (the stand-up) | every word of the line, lips on the words, a beat before the punchline, the laugh after it |
| 2, fast motion (the kickflip) | the board spins once, stays one board, lands under both feet, wheels down |
| 3, hands (the eggs) | five fingers throughout, the shell cracks and comes apart, the egg falls out of it into the pan, twice |
| 4, real or AI (the dog on the beach) | a believable dog (four legs, one tail), one frisbee, a real catch, water that splashes like water, the phone look |

A 1 is one slip on that line. A 0 is when the weak spot broke: the line was
wrong, the board fused to the shoe, the egg passed through the shell.

## How to score

1. Open the round's `blind/` folder only. Sort by name.
2. Watch each clip full screen, with sound, at least twice. The first watch is
   for the gut reaction, the second for the details.
3. Score that clip before you open the next one. Write the five marks (or the
   total) into `blind/scores.csv` straight away, with a few words in `notes`.
4. Score by clip number only. You do not know the model, and you should not
   try to guess.
5. Finish a round before you start the next. Do not go back and change a
   round's scores after you have seen later rounds: you would be scoring with
   hints about which clip is which.
6. Watch with the sound on and do not talk over it. Half of the result is the
   sound.

`scores.csv` looks like this. Fill the five marks, or just `total`. If you
fill both, `reveal.py` checks that they agree.

```
clip,brief,hard_part,face_and_body,sound,looks_real,total,notes
clip-1,2,1,2,2,1,,line came in late
clip-2,,,,,,6,
```

## Claude's part

- Claude can keep notes as you talk and write your numbers into `scores.csv`.
  It reads back each row it writes.
- Claude never scores a clip for you and never opens `.key.json`. It does not
  compare files in the round folder with the blind copies, and it does not
  guess which model is which.

## Value: points per 100 credits

The reveal divides each model's total by what its clips cost and multiplies by
100:

```
points per 100 credits = total / (credits per clip x rounds) x 100
```

Example: 34 out of 40 at 20 credits a clip over four rounds is
34 / 80 x 100 = 42.5. The same 34 at 160 credits a clip is 34 / 640 x 100 = 5.3.
The model with the most points per 100 credits is the best value. It is often
not the winner.

Credits count one clip per round. Errored attempts are listed in the attempts
column but not added to the cost, because platforms differ on whether a
failed generation is refunded. If yours charged you, mention it next to the
result.

With `--usd-per-credit` (your plan price divided by the credits it includes)
the reveal also shows dollars.

## Ties

Equal totals share a place (`#3=` for both). If two models tie for the win,
there are joint winners; say so rather than breaking the tie by price. The
value column already tells people which one is cheaper.
