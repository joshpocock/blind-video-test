# Nine models, four rounds

Which AI video model is best, judged blind on four things AI video is known
to get wrong: dialogue timing, fast motion, hands and the phone-footage look.
All nine models were run on Higgsfield in 2026-10.

## Lineup

The ids are the file names in each `round-N/` folder. `models.json` in this
folder holds the same list with credits.

| Id | Model | Credits a clip |
|---|---|---|
| 01-minimax-h3 | MiniMax H3 | 20 |
| 02-kling-3-0 | Kling v3.0 | 25 |
| 03-wan-3-0 | Wan 3.0 | 35 |
| 04-gemini-omni-flash-1-1 | Gemini Omni Flash 1.1 | 45 |
| 05-flux-3 | FLUX 3 Video | 80 |
| 06-grok-imagine-1-5 | Grok Video 1.5 | 80 |
| 07-seedance-2-0 | Seedance 2.0 | 120 |
| 08-seedance-2-5 | Seedance 2.5 | 160 |
| 09-kling-4-0 | Kling 4.0 | 20 |

Credits are what the Generate button showed for one 10 s, 16:9, 1080p clip
with sound, seen 2026-10-22 to 2026-10-26. Prices change. Read yours before
you start and put them in `models.json`.

## Settings

10 seconds, 16:9, 1080p, sound on, text only, for every model.

Closest-option notes (shown with the results, not put in the prompt):

- 10 seconds because one model (Gemini Omni Flash 1.1) stops at 10.
- Grok Video 1.5 had no aspect ratio option.
- MiniMax H3 rendered at 2K.

## Fairness rules

1. One prompt per round, word for word, never rewritten for a model.
2. The same duration, aspect, resolution and sound for all. Closest option if
   a model lacks one, noted above.
3. Text only: no reference images, no start frames, prompt-enhancer toggles off.
4. One take each. Rerun only on an error, and the rerun counts as an attempt
   (`-attempt-2` in the file name).
5. Original people and fictional brands only. No text on screen.
6. Download without watching. Shuffle, then score by clip number.

Pre-check: run each prompt once on a cheap model that is not in the lineup,
to catch burned-in captions or a misread camera move before the real run.

## Round 1, dialogue: the stand-up

1,006 characters.

```
A stand-up comedian on a small comedy club stage, filmed from the audience at seated eye height, 50 mm lens, shallow depth of field. A man in his forties with a shaved head, a thick black beard, black-framed glasses and a plain light grey t-shirt holds a microphone close to his mouth. One warm spotlight from above and slightly in front lights his face and shoulders and stays fixed; the red brick wall behind him falls into soft shadow. He starts talking right away, deadpan, in casual natural American English at normal speed with real comic timing, no long pause before the line: "I told my mom I'm a prompt engineer. She told her friends I'm unemployed." He shrugs, and the crowd bursts out laughing; the backs of two heads at the bottom of the frame shake with laughter. The camera pushes in slowly toward him. One continuous shot, no cuts, real-time motion. Sound: his voice through the mic with a little room echo, then the crowd laughing and a few claps. No music, no subtitles, no text on screen.
```

Hard part: every word, lips on the words, a beat before the punchline, the
laugh after it.

## Round 2, fast motion: the kickflip

962 characters.

```
A skateboarder kickflips down a set of seven concrete stairs in an empty city plaza. A lean man in his early twenties in a plain olive-green hoodie, light blue jeans and worn white sneakers rides a plain natural-wood skateboard fast toward the top of the stairs, pops the board, flicks it so it spins one full turn under his feet, catches it with both feet in the air and lands at the bottom, knees bending, all four wheels hitting the concrete, then rolls away past the camera. The camera sits low on the ground at the bottom of the stairs, 24 mm lens, and turns to follow him the whole way. Bright overcast afternoon: soft, even daylight from the sky and soft shadows. Pale grey concrete, a plain beige stone wall and two bare trees behind. One continuous shot, no cuts, real-time motion, no slow motion. Sound: wheels rolling on concrete, the sharp clack of the pop, the slap of the landing, the wheels rolling away. No music, no subtitles, no text on screen.
```

Hard part: the board spins once, stays one board, lands under both feet.

## Round 3, hands: the eggs

920 characters.

```
Close-up in a small diner kitchen, 85 mm lens at counter height, shallow depth of field. A black cast-iron pan sits on the stove with butter melted and foaming in it, and a small steel bowl beside it. A cook's right hand, weathered, with a rolled-up white sleeve, no rings and no watch, picks up a brown egg, cracks it one-handed on the rim of the pan, pulls the shell apart with his fingers, and the egg drops into the butter and starts to sizzle, the white turning opaque at the edges. He drops the shell into the bowl, picks up a second brown egg and does the same again. One warm lamp above the stove lights the pan from above and stays fixed; behind it, a wall of matte dark green tiles, soft and out of focus. The camera stays locked on a tripod. One continuous shot, no cuts, real-time motion. Sound: the crack of each shell, the egg hitting the butter, a steady sizzle. No music, no subtitles, no text on screen.
```

Hard part: five fingers throughout, the shell cracks and comes apart, the egg
falls out of it, twice.

## Round 4, real or AI: the dog on the beach

887 characters.

```
Casual phone video, filmed handheld by someone standing at the edge of the water on a sunny afternoon, with natural hand shake and the slightly flat look of a phone camera, everything in focus. A red frisbee flies out from behind the camera over the shallow waves. A golden retriever sprints after it across the wet sand and into the water, leaps and catches it in its mouth just above the surface, splashes down, then trots back toward the camera with the frisbee, tail wagging, and shakes the water off its fur. The person filming turns to follow the dog. Bright sun high on the left, small breaking waves, pale sand and a clear blue sky, nobody else on the beach. One continuous shot, no cuts, real-time motion. Sound: wind buffeting the phone mic, the waves, splashing paws, panting, and a woman off camera laughing and saying: "Good girl!" No music, no subtitles, no text on screen.
```

Hard part: a believable dog, one frisbee, a real catch, water that splashes
like water, the phone look.

## Run it

```
clips/
  models.json            copy of the one in this folder, with your prices
  round-1/ ... round-4/  01-minimax-h3.mp4 ... 09-kling-4-0.mp4
```

```
python blind.py clips 1        # after round 1 is downloaded, unwatched
python blind.py clips 2
python blind.py clips 3
python blind.py clips 4
# score each round's blind/scores.csv
python reveal.py clips --usd-per-credit <your price per credit>
```

36 clips. At the credits above, one clip on every model is 585 credits and
all four rounds are 2,340.
