# Ink review, round 1: product brief Stage 1 (Intake), clarity lens

**Reviewed:** `docs/intent/factor.md` (251 lines). I checked it against `docs/decisions.md`, `docs/design/feature-verdicts.md`, `docs/design/ui-brief.md` and the `/brief` templates in the plugin (read-only).

**Lens:** undefined terms, ambiguous sentences, cross-references that don't resolve, inconsistent names, and unlabelled inference (the brief's own source note promises these labels). Audience is internal and agent-primary, so em-dashes and stylistic tells are not findings, and nothing inside a Peter quote is flagged.

**What I checked and found clean, so these are not findings:**
- The NG-6 count: 37 Idea entries plus 105 Committed entries make 142.
- Every `D-NNN` cited exists in `decisions.md`.
- `docs/design/feature-verdicts.md` exists at `c60f8db`.
- `docs/research/calc-tools.md` and `engine-2026-10.md` exist.
- `P-RustDefault` resolves in the plugin canon.
- `spec_type: architecture` is a valid template value.
- The specops/delta-merge format note is template text.

## Findings

### F1 · high · SC-3's "100 ms" is Puck's number, stated as if it were Peter's
**Anchor:** SC-3, line 41; header line 37.
Peter's words are "target instant". Line 37 says SC-3 "is his answer on speed", not an option label. I grepped `docs/` and `CLAUDE.md` for "100 ms"/"100ms" and the only hit is this line, so nothing in the record supplies the number. The source note (line 13) promises that every interpretation is labelled **Puck's reading**, and SC-2 does label its threshold that way. SC-3 does not. A cold agent will read 100 ms as Peter's ruled budget and set a test gate on it.
*Suggested:* "**Puck's reading:** 'instant' is taken as under 100 ms…"

### F2 · high · The SC-3 check measures less than the SC-3 criterion claims
**Anchor:** SC-3, line 41.
The criterion runs "from the edit to the updated view", which takes in the solve, any re-layout (F-069 auto layout) and the render. The check only says "solve time recorded on every solve, plus a budget test". Two implementers would build different tests: one times the solver, the other times the whole path to the frame on screen. A solve-only test can pass while the criterion fails. Say which interval the budget covers, and whether it includes layout and render.

### F3 · high · "Machine", "megabase" and "node edit" are undefined, and the scale target depends on them
**Anchor:** PI-1 line 19; SC-2 line 40; SC-3 line 41.
- **"Machine."** "At least 5,000 machines in one plan" doesn't say whether it means building instances or diagram/recipe nodes. D-012's proposal says "One diagram node may stand for many machines". A plan with 5,000 building instances could be a few dozen nodes, which is a trivial solve. A plan with 5,000 nodes is a very different reference plan, both for the solver and for the diagram. The "generated reference plan" that SC-3 is also timed against can't be built until this is settled.
- **"Megabase."** PI-1 uses it before SC-2 defines it, and it is defined only through Puck's reading. A forward reference ("megabase scale, as SC-2 defines it") would fix the order.
- **"Node edit."** "Node" means two things in this brief. In the SC-3 sentence it is a diagram node. In the Extraction features it is a resource node (F-043 purity, F-044 Node inventory input, F-095 Resource node map). D-024 lists the edit kinds (pin a recipe, fix a machine count, cap an input).
*Suggested:* "a diagram edit as D-024 lists them: pin a recipe on a node, fix a machine count, cap an input".

### F4 · high · The SC-4 fixture is mis-stated and its source isn't cited
**Anchor:** SC-4, line 42.
- **Mis-stated.** It says "the 80/min-capped iron chain whose clocks are 8/9". The only source for this chain is `docs/design/ui-brief.md` lines 230–243, and there only the Smelters run at 8/9 (88.8888%). Downstream clocks are 75% × 8/9 = 2/3 (66.6667%) ("every downstream clock scales by 8/9"). A fixture author working from SC-4 alone would assert 8/9 on every node, and the check would then be wrong.
- **Not cited.** The chain isn't defined anywhere in the brief, so it doesn't resolve for a cold reader.

*Suggested:* "the iron chain in `docs/design/ui-brief.md` (Iron Ore capped at 80/min): Smelters ×3 at 8/9, every downstream clock scaled by 8/9".

### F5 · medium · "The exact clocks Peter would pick by hand" can't be computed, and it may clash with D-016's sizing rule
**Anchor:** SC-4 line 42; HC-4 line 50.
SC-4 is checkable only through its fixtures, so the phrase itself can't settle a case the fixtures don't cover. Peter's example is two machines at 75% for 1.5/min from 1/min machines. D-016 sizes "by fewest buildings or a count Peter sets". Whether "fewest buildings" lets a machine run above 100%, which would give one machine at 150% here, isn't stated. One reader says the default reproduces Peter's practice; another says the fixture contradicts the ruled default. Name the rule SC-4 holds the output to; how sizing works can stay with Frame. See Domain Question 2.

### F6 · medium · A non-goal contradicts a Committed feature by name: NG-4 against F-081
**Anchor:** NG-4 line 31; F-081 line 213.
NG-4 says "No walkthroughs or tutorials". F-081 "Guided tutorial and demo plans" sits in Committed (*later*). D-034 resolves this: a demo plan is allowed and a walkthrough is not. The brief doesn't carry that resolution to the F-081 line, so an agent reading the register could schedule a tutorial.
*Suggested:* add to F-081's line "(demo plans only; a walkthrough is out by NG-4 / D-034)".

### F7 · medium · NG-1 against F-004 "Splitter/merger behaviour simulation"
**Anchor:** NG-1 line 28; F-004 line 140.
NG-1 is titled "Not a simulation" and says splitter behaviour "comes back later as a separate check over a solved plan (… brain #3924)". F-004, a Committed feature with "simulation" in its name, isn't tied to that check. A reader can't tell whether F-004 *is* the #3924 check or a second, conflicting commitment.
*Suggested:* cross-link the two, on F-004's line and in NG-1.

### F8 · medium · The "Check:" lines are Puck's design, but the source note says nothing here is Puck's intent
**Anchor:** source note line 13; the *Check:* clauses on lines 39–43.
The check mechanisms are not Peter's words and not ruled decisions. They include the generated reference plan, the budget test, "no diff to the core model's crate", and the fixture choice. The source note says every field is Peter's, ruled, or labelled as Puck's reading, and that "nothing here is Puck's intent". The checks carry no label. A cold agent will treat them as ratified acceptance tests.
*Suggested:* label them as proposed checks for confirmation at the intake gate, the same way the tier mapping on line 89 is labelled.

### F9 · medium · The F-002 tier conflicts with D-017, the decision the brief cites
**Anchor:** F-002 line 98; HC-4 line 50 cites D-017.
The brief puts F-002 in Idea (*skip*), and that matches `feature-verdicts.md` @ `c60f8db` (line 6: `skip`). D-017's "Picker verdicts, 2026-10-08" list in `decisions.md` records F-002 as *later*. An agent that follows the D-017 cite gets the other answer. The brief looks right. The defect is in `decisions.md`, outside my write scope, so it needs reconciling there, or the brief should say which source wins.

### F10 · medium · NG-5 leans on D-019 as if it were ruled
**Anchor:** NG-5 line 32; HC-9 line 55; RP-4 line 77.
D-019 sits under **Open** in `decisions.md`. Its "Outcome (icons, first build)" is a partial ruling inside an open block. NG-5 cites it like a ruled decision, HC-9's list of open items leaves it out, and RP-4 lists it as open. A reader can't tell which part of D-019 is settled.
*Suggested:* "(D-019 Icons and map data, first-build outcome only; the block is open)".

### F11 · low · Decision cites mix "id and name" with "id only"
**Anchor:** line 13 promises "cited by `D-NNN` id and name". Bare ids appear at line 24 (D-017), SC-5 (D-002), and HC-2 through HC-8 (D-002, D-004, D-017, D-020, D-016, D-021, D-022, D-023, D-018, D-024, D-032, D-031, D-033).
Either apply the stated convention or narrow the promise (for example, name on first cite only).

### F12 · low · Terms a cold agent can't resolve from inside the brief
- **"Clock" / "clock speed"** (PI-1 line 19, SC-4). This is Satisfactory's per-machine speed percentage. It is never glossed, and in a multi-game brief (NG-3) a reader can't tell whether it is a game-neutral concept. D-007/D-008 treat it per game.
- **"Modeler"** (line 24). First used bare. The full name "Satisfactory Modeler" first appears at SC-1 (line 39), and the quote on line 21 spells it "modeller".
- **"Picker" / "picker verdicts"** (line 89). Not defined in the brief. `decisions.md` § Open explains it.
- **"Release note"** (lines 90, 94). Means the per-line "first build / eventually" label, but it reads as a changelog. "Release label" would avoid the clash.
- **"Structural fence"** (line 94). Undefined.
- **"Core-model run"** (EV-6, line 64). Undefined.
- **"First build"** (NG-2, NG-5, register). Never defined. It reads as "the set of *mvp* features", but nothing says what closes it.
- **"Self-declared at intake"** (Risk profile, line 72). Doesn't say declared by whom.

### F13 · low · EV-3 runs measured and observed claims together
**Anchor:** EV-3, line 61.
- **Measured and observed.** "Measured" heads the sentence, so it reads as covering "Modeler's slowness comes from its semantics, not its solver". D-017 records that claim as observed from Modeler's 2025-03-26 devlog, not measured.
- **"Factories."** "300 coupled factories" in D-017 is "300 coupled factory copies (141,600 columns)". Since SC-2's scale target rests on this evidence, "copies" matters to how far the number reaches.

### F14 · [ARCH-DEFERRED] · SC-5 "no diff to the core model's crate" / "declared per-game extension points"
**Anchor:** SC-5, line 43.
The crate doesn't exist yet (line 92: "no code exists"), and "declared extension points" is undefined. How the core crate is structured is a mechanism choice, so this goes to Frame.
The clarity point is the wording, though. "No change … beyond declared extension points" can be read two ways: adding a *new* extension point to the core is either allowed or a violation. The check ("no diff") takes the strict reading and the criterion text doesn't, so say which one is meant.

## Domain Questions

1. **For SC-2, what counts toward the 5,000?** Building instances, or diagram/recipe nodes? And roughly how many distinct nodes did Peter's largest build have? The answer decides what the reference plan looks like.
2. **For SC-4, when Peter sizes machines by hand, what decides the count?** Is it "never above 100%, spread evenly", or something else? Does that hold across power, shards and Somersloops? This is the rule the D-016 default has to reproduce.
3. **For SC-3, does "instant" cover the redrawn diagram (layout and render) or the recomputed numbers?** If the two can land at different times, which one must feel instant?
4. **Is F-004 the separate jam/starvation check that NG-1 and brain #3924 describe, or something different?**
