# Prompt rules: one prompt that is fair to every model

A blind test only means something if every model got a prompt it could follow.
A vague prompt rewards the model that guesses your taste. A prompt full of
traps (mirrors, flicker, smoke) punishes every model for something you are
not testing. These rules keep the prompt clear, so the round tests the one
weak spot it is meant to test.

Learned writing the four rounds in `round-ideas.md` and running them on nine
models (2026-10). The rules are general.

## Order: write it in playback order

**1. Subject, action, camera, look, sound. In that order.**
Why: models read a prompt roughly the way the clip plays. Who and where first,
then what happens, then how it is filmed, then how it looks and sounds. A
prompt that jumps around gets events out of order.

## Camera and time

**2. One camera move, written once.**
"The camera pushes in slowly toward him." Not a push, then an orbit, then a
tilt. Why: two moves in ten seconds get blended or one gets dropped, and then
you are scoring the camera, not the round.

**3. Say "One continuous shot, no cuts".**
Why: several models cut to a second angle by default. A cut you did not ask
for changes what you are judging.

**4. Say "real-time motion" (and "no slow motion" for action).**
Why: models drift into slow motion, which hides bad physics and makes fast
action look easy.

**5. Describe motion physically.**
"Pops the board, flicks it so it spins one full turn under his feet, catches
it with both feet in the air." Not "does an epic kickflip". Why: the
physical version is something every model can attempt and you can check frame
by frame.

## Dialogue

**6. Put any spoken line in double quotes, at the very start of the action.**
Why: a line buried at the end of the prompt often comes late, gets cut off at
the end of the clip, or is not said at all.

**7. Say the delivery.**
"Casual natural English at normal speed with real emotion, no long pause
before the line." Adjust the emotion to the scene ("deadpan, with real comic
timing"). Why: without it you get slow, flat, robotic reads, and long silence
before the first word.

**8. Write contractions as they are said.**
"I'm", "she's", "don't". Why: the model reads exactly what you write. "I am"
comes out stiff.

**9. One speaker per clip.**
Why: two people talking in one shot is where lines collide and get garbled.
Unless that is the weak spot you are testing, keep it to one voice.

## Light and look

**10. Describe light by what it does, from a real source that stays fixed.**
"One warm spotlight from above and slightly in front lights his face and
shoulders and stays fixed." Why: a named source with a direction gives every
model the same picture. "Stays fixed" stops the light from drifting or
pulsing.

**11. Never write "cinematic", "premium", "high-end", "epic" or "stunning".**
Why: those words mean nothing physical. Each model fills them in with its own
house style, so you end up judging the style, not the round.

**12. Name the lens, the camera height and the depth of field.**
"Filmed from the audience at seated eye height, 50 mm lens, shallow depth of
field." Why: it fixes the framing for every model.
Exception: a phone-footage round asks for "everything in focus" and the "slightly
flat look of a phone camera", and names no lens. The target is a phone.

**13. Make the subject contrast with its set.**
A different brightness or a different hue: a man in light grey against a
shadowed red brick wall, a brown egg against dark green tiles. Why: when the
subject and the background are the same tone, models merge them and edges
melt.

**14. Two or three objects, no more.**
Why: every extra object is one more thing that can morph, multiply or vanish,
and none of them is what you are testing.

**15. Concrete wardrobe, identical wording.**
"A plain olive-green hoodie, light blue jeans and worn white sneakers." Why:
"casual clothes" gets nine different outfits, and the face and body mark needs
something specific to check.

## Avoid

**16. Leave these out unless they are the weak spot the round tests:**

- **Shiny or mirrored surfaces** (glass tables, chrome, mirrors, wet floors):
  reflections are a hard test of their own.
- **Moving light** (candle flicker, leaf shadows, passing car lights, neon
  that buzzes): it reads as a glitch even when it is right.
- **Haze, smoke, fog, steam clouds**: they hide faces and hands, which hides
  the very failures you want to see.
- **Lens flares**: same problem, plus they look like an artefact.
- **Any text, logos or brand marks on screen**: most models misspell text, so
  it drags every score down on something you did not mean to test.

## Sound

**17. Put each sound next to the event that makes it.**
"The sharp clack of the pop, the slap of the landing." Why: listing sounds in
the order of the action is what gets them on time, and the Sound mark is about
timing.

**18. End with "No music, no subtitles, no text on screen."**
Why: some models add a music bed or burn in captions by default. Either one
makes the clips harder to compare.

## Length

**19. Keep it under about 1,000 characters.**
Why: some models cap the prompt at 2,500 characters, and a prompt that gets
cut off is not the same prompt. Shorter also means less for a model to drop.
The four example rounds are 887 to 1,006 characters.

Count it:

```
python -c "import sys; print(len(open(sys.argv[1], encoding='utf-8').read().strip()))" prompt.txt
```

## Before the real run

**20. Pre-check every prompt on one cheap model that is NOT in the lineup.**
Why: it catches prompt-level problems (burned-in captions, a camera move that
gets misread, a line nobody can say, a clip that comes back the wrong shape)
without you seeing any of the models you are about to judge. Fix the prompt
itself. Never write a different version for one model.

## The template

```
<Subject and place, with lens, camera height and depth of field>. <Who, with
concrete wardrobe>. <Light: one real source, where it is, what it lights,
"stays fixed">; <the set, in contrast with the subject>. <Action, starting with
any line in double quotes and its delivery, described physically>. <One
camera move>. One continuous shot, no cuts, real-time motion. Sound: <each
sound next to its event>. No music, no subtitles, no text on screen.
```

## Quick check before you hand it over

- [ ] Subject, action, camera, look, sound, in that order
- [ ] One camera move, once
- [ ] "One continuous shot, no cuts" and "real-time motion"
- [ ] Any line in quotes, at the start of the action, with its delivery
- [ ] Light from a real source that stays fixed; no "cinematic" or "premium"
- [ ] Lens, height, depth of field (or "everything in focus" for phone footage)
- [ ] Subject contrasts with the set; two or three objects
- [ ] No mirrors, moving light, haze, flares, text or logos (unless that is the test)
- [ ] Each sound next to its event; ends "No music, no subtitles, no text on screen."
- [ ] Under about 1,000 characters
- [ ] Original people, fictional brands
