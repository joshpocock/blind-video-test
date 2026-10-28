# Round ideas: one weak spot per round

A good round tests one thing AI video is known to get wrong, and anyone can
judge it in ten seconds without knowing anything about AI. Write each round's
prompt with `prompt-rules.md` and its hard part line with `scorecard.md`.

What to skip: battles, monsters and other spectacle (every clip "looks cool",
so nothing separates the models), couples in restaurants, animated family
ads and AI influencer clips (done to death, and hard to judge on one thing).

## The worked example: four rounds, nine models

Run in 2026-10 on nine models, 10 s, 16:9, 1080p, sound on, text only, one
take each. Lengths are 1,006, 962, 920 and 887 characters, inside every
model's limit.

### Round 1, dialogue: the stand-up

Weak spot: a spoken line with timing. Models drop words, miss the lips, and
rush or stall the joke.

```
A stand-up comedian on a small comedy club stage, filmed from the audience at seated eye height, 50 mm lens, shallow depth of field. A man in his forties with a shaved head, a thick black beard, black-framed glasses and a plain light grey t-shirt holds a microphone close to his mouth. One warm spotlight from above and slightly in front lights his face and shoulders and stays fixed; the red brick wall behind him falls into soft shadow. He starts talking right away, deadpan, in casual natural American English at normal speed with real comic timing, no long pause before the line: "I told my mom I'm a prompt engineer. She told her friends I'm unemployed." He shrugs, and the crowd bursts out laughing; the backs of two heads at the bottom of the frame shake with laughter. The camera pushes in slowly toward him. One continuous shot, no cuts, real-time motion. Sound: his voice through the mic with a little room echo, then the crowd laughing and a few claps. No music, no subtitles, no text on screen.
```

Hard part: every word, lips on the words, a beat before the punchline, the
laugh after it (not before).

### Round 2, fast motion: the kickflip

Weak spot: a fast object in the air. Models glue the board to the shoes,
spin it twice, or swap it for a second board.

```
A skateboarder kickflips down a set of seven concrete stairs in an empty city plaza. A lean man in his early twenties in a plain olive-green hoodie, light blue jeans and worn white sneakers rides a plain natural-wood skateboard fast toward the top of the stairs, pops the board, flicks it so it spins one full turn under his feet, catches it with both feet in the air and lands at the bottom, knees bending, all four wheels hitting the concrete, then rolls away past the camera. The camera sits low on the ground at the bottom of the stairs, 24 mm lens, and turns to follow him the whole way. Bright overcast afternoon: soft, even daylight from the sky and soft shadows. Pale grey concrete, a plain beige stone wall and two bare trees behind. One continuous shot, no cuts, real-time motion, no slow motion. Sound: wheels rolling on concrete, the sharp clack of the pop, the slap of the landing, the wheels rolling away. No music, no subtitles, no text on screen.
```

Hard part: the board spins once, stays one board, and lands under both feet.

### Round 3, hands: the eggs

Weak spot: fingers doing a fine task. Models add fingers, and eggs pass
through shells.

```
Close-up in a small diner kitchen, 85 mm lens at counter height, shallow depth of field. A black cast-iron pan sits on the stove with butter melted and foaming in it, and a small steel bowl beside it. A cook's right hand, weathered, with a rolled-up white sleeve, no rings and no watch, picks up a brown egg, cracks it one-handed on the rim of the pan, pulls the shell apart with his fingers, and the egg drops into the butter and starts to sizzle, the white turning opaque at the edges. He drops the shell into the bowl, picks up a second brown egg and does the same again. One warm lamp above the stove lights the pan from above and stays fixed; behind it, a wall of matte dark green tiles, soft and out of focus. The camera stays locked on a tripod. One continuous shot, no cuts, real-time motion. Sound: the crack of each shell, the egg hitting the butter, a steady sizzle. No music, no subtitles, no text on screen.
```

Hard part: five fingers throughout, the shell cracks and comes apart, and the
egg falls out of it, twice.

### Round 4, real or AI: the dog on the beach

Weak spot: the everyday phone look. Models make everything look like a
movie, and animals and water give them away.

```
Casual phone video, filmed handheld by someone standing at the edge of the water on a sunny afternoon, with natural hand shake and the slightly flat look of a phone camera, everything in focus. A red frisbee flies out from behind the camera over the shallow waves. A golden retriever sprints after it across the wet sand and into the water, leaps and catches it in its mouth just above the surface, splashes down, then trots back toward the camera with the frisbee, tail wagging, and shakes the water off its fur. The person filming turns to follow the dog. Bright sun high on the left, small breaking waves, pale sand and a clear blue sky, nobody else on the beach. One continuous shot, no cuts, real-time motion. Sound: wind buffeting the phone mic, the waves, splashing paws, panting, and a woman off camera laughing and saying: "Good girl!" No music, no subtitles, no text on screen.
```

Hard part: a believable dog, one frisbee, a real catch, water that splashes
like water, and the phone look. (This is the one prompt with everything in
focus and no lens: the target is a phone.)

## More rounds

Each has the weak spot, a sketch of the scene and the hard part line. Write
the full prompt with `prompt-rules.md`. Where a round's weak spot is on the
"avoid" list (text, a mirror, two speakers), that one thing is allowed
because it is the test; keep everything else in the rules.

1. **Text on a sign, read aloud.** A market stall owner taps a hand-painted
   wooden sign that reads "FIGS 3 FOR 2" and reads it out to a customer.
   Hard part: the sign is spelled right and stays the same, and she says
   exactly what it says.

2. **A crowd.** About a dozen people cross a wide zebra crossing from both
   sides at once, filmed from a fixed camera on the corner at head height.
   Hard part: the number of people stays the same, nobody walks through
   anybody, and no face melts as they pass.

3. **A pour.** A bartender pours a dark beer from a brown bottle into a
   tilted pint glass on a wooden bar, straightening the glass as it fills.
   Hard part: one unbroken stream from bottle to glass, the level only rises,
   and a head of foam forms on top.

4. **A walk past a mirror.** A woman in a mustard coat walks down a narrow
   hallway past a tall mirror on the wall, camera following from behind.
   Hard part: the reflection moves when she moves, faces the right way, and
   her coat is the same before and after the mirror.

5. **Juggling.** A street performer in a striped shirt juggles three red
   balls in a steady pattern in an empty park, locked camera at chest height.
   Hard part: three balls the whole time, arcs that fall like real weight,
   and every catch in a hand.

6. **Two speakers, one shot.** Two old men at a chess table in a park, one
   moves a piece and says a short line, the other answers with one line.
   Hard part: each line comes from the right mouth, in turn, with two
   voices that stay different.

7. **Sound on the beat.** A drummer in a small rehearsal room plays a slow,
   simple rock beat on a kit, camera at the side of the kit.
   Hard part: every hit you hear lands as a stick hits a drum or cymbal,
   and the beat stays steady.

8. **A product shot.** A made-up product with a made-up name printed on it
   (for example a matte cream ceramic mug with "HALDEN" on the side) turns
   once on a wooden turntable, plain backdrop, one soft key light.
   Hard part: the product keeps its exact shape and colour, and the made-up
   name is spelled right every time it faces the camera.

9. **A camera orbit.** A potter at a wheel in a small studio raises a clay
   cylinder with both hands while the camera makes one slow half-circle
   around her. Hard part: the clay rises under her hands like clay, and the
   room behind her is the same room as the camera comes around.

10. **An emotional face, no words.** An older man in a cardigan sits at a
    kitchen table and reads a handwritten letter (its back to the camera);
    over ten seconds his face goes from neutral to tears.
    Hard part: a gradual, believable change of expression, and he stays the
    same person the whole time.

## Picking rounds for "best for X"

When the user asks which model is best for one kind of shot, make every round
a different hard case of that kind:

- **Dialogue:** a line with timing (round 1), two speakers (idea 6), a sign
  read aloud (idea 1), a whispered line in a quiet room.
- **Product shots:** a product turn (idea 8), a pour (idea 3), hands using
  the product (round 3's hands, applied to the product), the product in
  phone footage (round 4's look).
- **Action:** fast motion (round 2), a crowd (idea 2), juggling (idea 5), a
  camera that has to follow (round 2's turning camera).
