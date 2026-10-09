# Pixel review, round 3: docs/intent/factor.md (product altitude, Intake)

Lens: user-facing requirements, interaction model, accessibility. Layout, visual and toolkit calls are [ARCH-DEFERRED] and not judged.

Range (re-runnable): `docs/intent/factor.md` lines 1-384 read in full; `scratch/factor-review-r2/pixel.md` read in full. Not re-opened this round: `docs/decisions.md`, `docs/design/*`, `CLAUDE.md`. Nothing here claims a state of the design docs. The C1 to C6 routing was taken from the brief's "Dismissed review flags" paragraph, not checked against the design files. No running UI exists; all findings are from reading the brief.

## Round-2 dispositions

- **N1 (HC-10 had no Check): resolved.** HC-10 now has a Check: contrast measured per token at each Spec, plus a keyboard-only walk of the SC-3 edit loop. No fix-induced problem.
- **N2 (D-036 spike must test the accessibility API): resolved.** HC-9 says the spike records each toolkit's screen-reader support, including for a custom-drawn diagram. Residual: the spike has no pass/fail consequence. That is [ARCH-DEFERRED] and not raised.
- **N3 (stale numbers undefined): partly resolved.** SC-3 now says numbers from the previous solve are marked stale, never shown as current. The wording leaves a gap, and the fix introduced it: see F1. F3 adds a smaller residual.
- **N4 (SC-9 pin kinds): resolved, with one omission.** SC-9 now covers every kind of value, and the Check runs per kind. The listed kinds drop the supply cap, which was in Peter's own question: see F2. Fix-induced.
- **C1 to C6:** carried in "Dismissed review flags" as routed to design work (task #3933). Accepted as routing. C1 and C4 now also bear on F1 and F2, so the design work should read them together.

## Findings

### F1. [medium] The stale marker ends before the diagram's own numbers are replaced (fix-induced)
- SC-3 splits the edit into two deadlines: new numbers within 100 ms at p95, and the redraw "within 1 second", outside the 100 ms. The stale rule is "Until the new numbers land, numbers from the previous solve are visibly marked as stale."
- The diagram carries numbers too: edge rates, node counts, clocks. After the new numbers land (for example in the inspector or status area), the diagram can keep showing the old ones for up to another 900 ms. By the sentence as written, those old diagram numbers are no longer covered by the stale rule. That is the mixed fresh and stale state N3 asked to close, left open for the diagram. Peter reads these numbers to build in game (EV-5), so a stale edge rate read as current is a build error.
- Recommend: the stale mark ends per displayed number, when that number is replaced, not when the solve finishes. One clause is enough: "a number is marked stale until the display of that number has been replaced." Whether the mark is dimming, a badge or something else is [ARCH-DEFERRED].
- Anchor: SC-3 (Window, Redraw).

### F2. [low] SC-9's list leaves out the supply cap and external supply (fix-induced)
- Peter was asked about "a recipe, a machine count, a cap". The new list is recipe, machine count, clock (with shards and Somersloops), target rate, and miner or extractor settings. A per-resource cap (F-009) and on-hand or external supply (F-008) are both first-build *mvp* and are values Peter types. Neither is named, and "miner or extractor settings" does not obviously include them. D-018 puts the ceiling on the extractor, but F-009 and F-008 are still separate inputs.
- The Check is "for each kind", so the list is what makes it complete. An omitted kind is an untested kind, with no signal.
- Recommend adding caps and external-supply rates to the list, or stating that they are plain inputs and not pins, with the reason. Recommend adding them: the release control is the same, as I said in round 2.
- Anchor: SC-9; F-008; F-009.

### F3. [low] The stale state has no exit if the solve fails or runs long, and is only "visible" (fix-induced)
- "Until the new numbers land" assumes they land. If a re-solve is infeasible, errors or exceeds 1 s, the numbers stay stale with no stated end state. SC-3 treats over 100 ms as a measurement failure, not as a user-facing state. The user needs to be told the display is stale because the solve did not finish, and not left reading the old numbers with a mark and no explanation.
- "Visibly marked" is a sighted-only statement. HC-10 says the toolkit can expose the controls and the diagram to a screen reader. The stale state is one more thing it must expose, so a screen-reader user is not given stale numbers as current. One clause covers it: the stale state is available to assistive technology, and the solve-did-not-finish case has a named state.
- Anchor: SC-3; HC-10.

### F4. [low] SC-7 does not say where the named error appears
- "Rejected with a named error that says which file and what is wrong" is checked by seeded fixtures. A desktop app has no console for the player. If the error lives only in a log or a test assertion, the check passes and Peter sees nothing. This is not fix-induced; I did not raise it before.
- Recommend one clause: the error is shown to the user in the app, and the Check asserts that, not only that an error value exists.
- Anchor: SC-7.

## Domain Questions

1. **Target size is still unrecorded (carried from round 2).** HC-10 and HC-11 bind the canon accessibility floor at first share, but no number is recorded. The canon floor reads 44 px. The UI brief proposed 24 px minimum and 32 px preferred for a pointer-driven desktop app. Does the floor Peter accepted include 44 px, or is 24/32 px the desktop reading? Recommend 24/32 px for the desktop first build, 44 px at the phone layout (F-085), written as a ruling so the first-share gate has a number to test against.
2. **OS text size (carried from round 2).** Should the first build honour the operating system's text-size setting, given F-079 (themes and display settings) is *later*? Recommend yes in the sense that nothing breaks when text grows. A user-chosen scale stays *later*. HC-7 already shapes in CJK and Hindi, where this matters.
3. **Pin kinds are Puck's reading, not a ruling.** SC-9 labels the extension to every kind of value as Puck's reading. Recommend asking Peter to confirm it with the F2 additions, since the Check and the mark-in-data requirement both depend on the list.
