# Pixel review, round 2: docs/intent/factor.md (product altitude, Intake)

Lens: user-facing requirements, interaction model, accessibility. Layout, visual and toolkit calls are [ARCH-DEFERRED] and not judged.

Range (re-runnable): `docs/intent/factor.md` lines 1-299 in full; `scratch/factor-review-r1/pixel.md`; `docs/design/ui-brief.md` in full; `docs/design/mockups/handoff-round1/README.md` in full; `docs/design/mockups/handoff-round1/screenshots/01-S1-factory-view.png` (dark; the light screenshot 02 was not opened); `docs/design/mockups/project/factor-tokens.css` (grep of colour, size and type tokens only); `S1FactoryView.dc.html` by grep only (font-size census, aria/role count). S2, S3, S5, S6 and the states sheet do not exist yet, so nothing is said about them. Contrast ratios below were computed by me from the declared token hex values with the WCAG relative-luminance formula, on a control pair (dark text on bg) that returned 13.71, matching the token file's 13.6 note. No running UI exists; the PNG is a design render, not a build.

## Round-1 dispositions

- **F1 (no accessibility requirement): resolved by HC-10.** Two residuals below (N1, N2).
- **F2 (assistive-tech and diagram access silent): carried as Q-F5. Accepted** as a Frame question. HC-10 names screen readers and gives the enforcement trigger (first share), so the DF1 trip-wire exists. My promised UI-brief fix is **not done** (see C1). N2 covers the toolkit link.
- **F3 (SC-3 endpoint): resolved.** Numbers under 100 ms, redraw may follow, an external instrument times it. N3 is a small fix-induced residual.
- **F4 (NG-4 versus F-081): resolved.** NG-4 carries the D-034 carve-out and F-081 is annotated.
- **F5 (set-by-you versus set-by-factor): resolved by SC-9.** N4 is a fix-induced scope gap.
- **F6 (Problems strip): dismissed. I agree.** It is a UI-brief defect, and naming of problems is already in scope through SC-2 (every shortfall, surplus and unhandled byproduct named) and D-023. Note the mockup README now draws the strip in S1 and S2, so the question has moved into the design work. Peter should confirm the strip there, and the UI brief should say F-013 and F-059 are *shape*.
- **F7 (SC-2 units and legibility): carried as Q-F5. Accepted.** SC-2 now defines a machine as a building instance, which fixes the unit. It still has no load-time budget and no findable/readable clause. Both are covered only by Q-F5's wording "diagram legibility at SC-2 scale", so keep that wording on the Frame.
- **F8 (SC-1 parity list): partly resolved.** SC-1 now defines parity as the first-build Committed set, labelled Puck's reading. That is a list of what factor will have, not of what Peter needs from Modeler, and D-035 (factory organisation, his named complaint) is open while F-053 and F-054 are first build. Low; the "a 'no' names the missing capability" clause handles the gap.
- **F9 (rounding direction): resolved** by Peter's ruling (round to nearest, 88.8889%). It creates contradiction C2.
- **F10 (shared later unbounded): partly resolved.** HC-7 and HC-10 bound localisation and accessibility. First run on a machine with no game install is still unaddressed (NG-5, D-026). Low, unchanged.

## Findings

### N1. [low] HC-10 has no Check line, and "shaped" has no observable test
- Every other constraint states what is verified or is a ruled outcome; HC-10 says "supports screen readers, keyboard-only use and readable contrast from the start" with nothing a reviewer can fail. "Shaped now" is the silent-failure class: a mockup can be built with no accessible structure and nothing fires until the first share.
- Recommend a Check line in the brief's style, for example: at each Spec, the measured contrast per token pair is written down, and the keyboard-only walk of the SC-3 edit loop is done, so "enforced on share" is a re-run and not a first-time discovery.
- Anchor: HC-10. Fix-induced: yes (the new constraint arrived without a check).

### N2. [medium] The toolkit decision (D-036) is the thing that can foreclose HC-10, and HC-9 does not say it is a criterion
- HC-10 says the toolkit supports screen readers and keyboard use "from the start". HC-9 lists the toolkit as open with a spike pending, and does not say the spike must test the accessibility API. A toolkit that cannot expose a tree is not cheaply fixed after the spike, and the check is not computable later without the spike having looked.
- Recommend one line in HC-9 or the Frame: the D-036 spike records the toolkit's accessibility-API support, including for a custom-drawn diagram. [ARCH-DEFERRED] on which toolkit.
- Anchor: HC-9; HC-10; D-036. Fix-induced: yes.

### N3. [low] SC-3 leaves the not-yet-updated state undefined for numbers outside the diagram
- Numbers may be on screen within 100 ms, but the UI brief dims the old diagram while re-solving. If the inspector and status bar show the new values while the dimmed diagram shows old ones, the user reads a mix as current. The brief need not design it, but SC-3 or the Frame should say that a displayed number is never stale while labelled current.
- Anchor: SC-3. Fix-induced: yes (the "redraw may follow" split created the mixed-state window).

### N4. [low] SC-9 lists three pin kinds, the interaction has more
- SC-9 names recipe, machine count and cap. The UI brief and mockup also let Peter set clock mode, power shards, somersloops, target rates and "arrives from elsewhere" rates. If those are pins, the check must cover them; if they are plain inputs, the line between "a value I set" and "a pin" needs a sentence. The UI brief's glossary-level definition (Pin) is "recipe, machine count, cap".
- Recommend "(for example)" or a full list. The check line is per pin kind, so the list is what makes it complete.
- Anchor: SC-9; Glossary "Pin". Fix-induced: yes.

## Contradictions: UI brief or mockups versus the product brief (follow-ups for the design work, each separate)

- **C1. UI brief constraint 13 predates HC-10.** It covers contrast, keyboard, focus and target size only. It omits screen-reader semantics, OS text-size honouring, and a reduced-motion behaviour for the dimmed re-solving state (my round-1 F2 admission; still unfixed). HC-10 names screen readers. Owner: Pixel, UI brief.
- **C2. 8/9 is shown as 88.8888%; the brief now rules 88.8889%.** `ui-brief.md` §2, §3 S2, §7 and §8 paste block, and the mockup README S2 plan ("88.8888% (8/9)"), all use truncated figures. SC-4's ruling is round to nearest. Every display example for a non-terminating clock needs recomputing (88.8889%, and 66.6667% already rounds correctly). Peter's own quote in PI-1 stays as his words.
- **C3. Typefaces and caps styling versus HC-7.** HC-7 shapes in Chinese, Japanese and Hindi. The mockup's labels are Cinzel in caps with 0.1em tracking (README, Fidelity), body Source Sans 3 and numbers IBM Plex Mono. Cinzel is a Latin display face and the other two do not cover CJK or Devanagari either (my knowledge, not checked against the font files). Forced caps does nothing in those scripts, and letter-spacing breaks Devanagari joining. The UI brief constraint 7 covers label length (40%) only. Follow-up: the spec must state a fallback stack and that tracking and caps apply to Latin labels only.
- **C4. Pin marker covers only some pin kinds in the mockup.** S1 marks Machines and Clock as "Set by factor" with a Pin button, but the supply Cap field, the recipe swap and the target rows carry no set-by-you marker or release. SC-9 names cap and recipe. S1 must show them, or the spec must say where they appear.
- **C5. Text size.** The token file defines 10px (`--text-micro`) and the S1 markup has 14 uses of it, 7 of 10.5px and one of 9px, including keyboard hints and edge labels; the diagram is read at a glance beside a game. HC-10 says "readable". The UI brief sets no minimum text size. Follow-up: the spec states a floor for text that carries data (edge rate labels especially). No ratio problem here; the ratios hold (below).
- **C6. Problems strip versus *shape* tiers.** The mockup and UI brief draw it as first-round (see F6). Not a brief contradiction while the brief says problems are named (SC-2), but F-013 and F-059 are *shape* and the UI brief should say so beside the strip. Routed, not raised against the brief.

Measured contrast, from the declared tokens (mine): dark text on bg 13.71; ghost on surface 5.07; control border on surface 3.13 (token note says 3.2, the margin to the 3:1 floor is 0.13, so any small shift in surface tone fails it); focus on surface 9.74; shortfall on surface 6.43. Light: ghost on bg 5.53; control border on surface 4.16, on bg 3.68; shortfall on bg 5.52; byproduct on bg 5.20; ok on bg 5.22; focus on bg 12.06. Not measured: surplus, accent-fill with on-accent, tinted backgrounds, the light-theme canvas. The mockup's own notes were not accepted as the measurement.

## Domain Questions

1. **Target size.** HC-10 binds the canon accessibility floor on first share. The UI brief proposes a 24px minimum hit area (WCAG 2.2) with 32px preferred, for a pointer-driven desktop app, against the 44px touch floor. Does the floor Peter accepted include 44px, or is 24/32px the desktop reading? Recommend 24/32px for desktop, 44px at the phone layout (F-085), and record it as a ruling so the gate has a number.
2. **Text size and OS settings.** Should the first build honour the operating system's text-size setting, given F-079 (interface scale) is *later*? Recommend yes in the sense that nothing breaks when text grows, and a user-chosen scale stays *later*.
3. **Pin kinds (N4).** Is every value Peter sets on a node or in Supply a pin (clock mode, shards, sloops, target rates included), or only recipe, count and cap? Recommend all of them, because the release control is the same.
