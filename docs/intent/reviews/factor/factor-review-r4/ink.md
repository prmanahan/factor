# Ink review, round 4: product brief Stage 1 (Intake), clarity lens

**Reviewed:** `docs/intent/factor.md` at `e8912b4` (387 lines). I checked it against:
- `docs/decisions.md`: D-004, D-016, D-018, D-022, D-024, D-028 and D-031;
- `CLAUDE.md` in this worktree;
- `docs/design/feature-verdicts.md`: F-006, F-007, F-009, F-032, F-043 and F-044;
- my round-3 review;
- `git diff 93d6c53 HEAD` over the brief and `decisions.md`, which is the round-6 change set.

I didn't open the other round-4 reviews.

**Lens:** the same as rounds 1 to 3. I looked for ambiguous phrasing, undefined terms, cross-references that don't resolve, inconsistent names and unlabelled inference. The audience is internal and agent-primary, so stylistic tells aren't findings. Nothing inside a Peter quote or a Peter option label is flagged.

**Audit of what the restructure removed.** Range: every `-` line in the success-criteria hunk (`@@ -34,69`) and the HC-10/HC-11 hunk (`@@ -126,18`) of `git diff 93d6c53 HEAD -- docs/intent/factor.md`. I traced each one to where it went: kept in the criterion, moved to FQ-7 or FQ-10, or gone. R4-5, R4-6 and R4-7 come from the "gone" column.

**Checked and clean:**
- **No stale ids.** `grep -rn 'Q-F[0-9]' docs CLAUDE.md` returns nothing, and the control `grep -c 'FQ-8' docs/intent/factor.md` returns 3.
- **No stale "first share" phrasing.** `grep -n 'first share' docs/intent/factor.md` returns nothing. The same grep for `on share` hits line 117, which is Peter's option label, so the instrument works.
- **`I-2` is unique.** `grep -rnw 'I-2' docs CLAUDE.md` hits only line 234.
- **Gate references resolve.** `grep -rnw -e 'Gate A' -e 'Gate B' docs CLAUDE.md` hits lines 122, 124, 125, 155, 168 and 199 of the brief and line 129 of `decisions.md`, and every hit names a gate HC-11 defines. Whether the hits agree on what each gate contains is a separate question; see R4-3.
- **Worktree `CLAUDE.md`** carries D-018 as amended (line 43).
- **FQ-10's attribution** of the 9/min case is correct: `grep -n '9/min' scratch/factor-review-r3/*.md` hits Glitch line 20 and Warden line 16.

## Round-3 dispositions

- **R3-1: resolved in the brief.** Targets are out of the pin list and caps are re-described (SC-9 line 81, F-009 line 282). Residuals outside the brief are in R4-9, and the fix-induced follow-ons are R4-2 and R4-9.
- **R3-2: resolved.** HC-11 line 130 and RP-3 line 167 now agree on per-slice reviews. The gate split opens a separate problem (R4-3).
- **R3-3: resolved.** The pinned count is settled by Peter's ruling, and the recipe swap is a labelled **Puck's reading** (line 69). The shard follow-on is R4-1.
- **R3-4: resolved.** "Missing reference" is gone, and line 76 leaves owner ids to FQ-4.
- **R3-5: resolved.** Line 79 reconciles rounds 2 and 5, "whichever comes first" is gone, and SC-3 line 53 puts the save inside the window.
- **R3-6: partly resolved.** The stale rule now covers every displayed value and is labelled. Which surface the numbers must be "shown" on is still unsaid: FQ-10 line 213 carries timing, not surface (low, no new finding).
- **R3-7: resolved by the move.** FQ-10 line 208 carries the start states and the 9/min and 10/min cases.
- **R3-8: resolved.** The header covers rounds 1 to 6, and SC-5's rule is labelled. The new label losses are R4-7.
- **R3-9: partly resolved.** SC-1, D-022, D-016, "largest connected part" and "more than one node's ceiling" are fixed. The 291 "machine recipe", "never typed" and the release-note glossary entry are still open, carried in R4-9.

## Findings

### R4-1 · medium · fix-induced (round 6: shard rule, pinned-count ruling) · Shards: a clock pin or headroom? SC-6 conflicts in both of its cases
**Anchor:** SC-6 lines 64, 65 and 66; SC-9 line 81; D-018 line 182 (Peter's quote); F-032 line 304; I-2 line 234.

Take a smelter where Peter has placed one shard and hasn't typed a clock, and raise the target past what the kept machines make at 100%. The answer depends on whether the count is pinned, and each case has its own conflict.
- **Count not pinned.** There's no shortfall, so only line 64 ("Add machines") applies: factor adds machines and re-clocks all of them "at or below 100%". That clocks the shard machine down to 100% or below and throws away the headroom Peter placed the shard for. Peter's D-018 model, below, treats a placed shard as usable range.
- **Count pinned.** There's a shortfall, so lines 65 and 66 both apply, and they disagree:
  - Line 65 says a shortfall's fix "may use shards already placed", which reads as permission to run the shard machine above 100%.
  - Line 66 allows above 100% "only where Peter has also pinned a clock". Under SC-9, "clock (including shards and Somersloops)" is one pin kind. So a placed shard is either not a clock pin, and line 66 forbids using it, or it *is* a clock pin, and the clock is fixed and can't move to cover anything.

Peter's own model in D-018 treats the two separately. Shards set the range ("If i add three shards that is 250% of the 120, so 300"), and the clock moves inside it ("I can change that value from 0-300 manually to a percentage"). That's headroom, not a fixed value. SC-9's grouping fuses the two.

Somersloops sit in the same group, but they change material flow and are set before the solve (D-016), so they aren't a clock either.

Separately, **F-032 Power shard count and budget** is Committed *mvp*. Its verdict text is "Count the power shards a plan needs and optionally plan within a shard budget (prefer 100% clocks)". Planning within a budget means factor places shards. That sits beside "never added by factor on its own" and beside I-2 (automatic shard allocation, Idea tier). One reading makes F-032's budget the "explicitly asks it to shard" case. Another reduces F-032 to counting the shards Peter placed. The brief doesn't say which.

*Suggested:*
- Split SC-9's pin kind into "clock" and "shards placed", and Somersloops into their own kind.
- State whether placed shards are headroom that line 64's "at or below 100%" yields to.
- State F-032's standing against the shard rule (Domain Question 1).

### R4-2 · medium · fix-induced (round 6: "targets are not pins", F-009 re-description) · Factor chooses targets in two *mvp* features, and one of them types a raw amount
**Anchor:** SC-9 line 82; glossary line 175; HC-4 line 101; F-006 line 279; F-007 line 280.

SC-9 line 82 says targets "are inputs Peter adds or removes, so there is no factor's choice to release them back to". Two Committed *mvp* features have factor choose the output:
- **F-006 Maximize output under limits:** "Instead of a target rate, maximise production…"
- **F-007 Scale targets to a pinned input:** "Type how much of a raw resource you actually have and the targets scale to consume exactly that."

In those modes, an output rate *is* factor's choice. So whether Peter can pin one, and what releasing it means, is open again.

F-007 also collides with round 6 in three ways:
- Its name says "pinned input".
- Its verdict text has Peter *type* a raw amount.
- HC-4 says a raw ceiling is "never typed", and F-009 was re-described as "not by typing a cap".

F-009 was re-described and F-007 wasn't. So a cold agent building F-007 will build the typed raw limit that F-009's re-description removed. That's R3-1's class, on a feature the round-6 fix didn't reach.

*Suggested:*
- Scope line 82 to target mode ("in target mode, targets are inputs…").
- Re-describe F-007 the way F-009 was, or state that F-007's typed amount is a different thing from a cap (Domain Question 3).

### R4-3 · medium · fix-induced (round 6: HC-11 split) · The legal obligations fire only at Gate A, but Gate B's event can carry them first
**Anchor:** HC-11 lines 124 and 125; NG-5 line 32; RP-4 line 168.

- **Order.** The two events aren't ordered. Peter can hand a build to a friend (Gate B) before the repo has any public remote (Gate A). That build is a distribution of factor, which raises the licence (D-025). If it ships generated data files or icons, it also redistributes game data and art (D-019, D-026). HC-11 lists the licence and redistribution only under Gate A, so in that order nothing fires them. NG-5 already frames the data question by Gate B's event ("how it reaches anyone but Peter is open (D-026)"), while HC-11 files D-026 under Gate A. Two readings fit:
  - the legal items fire on whichever event comes first;
  - a shared build is assumed to carry no game data or art.

  The brief should say which.
- **"Runs a build" is undefined.** It could mean a binary Peter produced, or a build anyone compiles from source. After Gate A, anyone can clone and build without Peter knowing, so Gate B's event as worded can't be observed. FQ-8 has to fire on something it can see. A definition such as "Peter first gives a build to anyone else" would give it one.
- **RP-4 against Gate A.** RP-4 says all of its contents are "fired by Gate A", and that includes community data inputs (D-028). Gate A's list on line 124 doesn't name D-028.

*Suggested:*
- Add "whichever event comes first" for the legal items, or list them under both gates.
- Define "runs a build".
- Add D-028 to Gate A (Domain Question 4).

### R4-4 · medium · fix-induced (round 6: node-ceiling ruling, F-009 re-description) · "A resource node's ceiling" isn't defined, and "cap" and "ceiling" now mean different things in different places
**Anchor:** SC-6 line 67; HC-4 line 101; SC-4 line 59; D-018 line 184 (Puck's prose, not Peter's); F-043 line 315; F-044 line 316.

**Which ceiling?** HC-4 says an extractor's ceiling "comes from its extractor, node purity and clock". When the clock or the extractor type isn't pinned, SC-6's "demand beyond a resource node's ceiling" has at least three readings:
- the rate at the current extractor and the current clock;
- the rate at the current extractor at 100%, or at the maximum the placed shards allow;
- the rate at the best extractor the plan has unlocked.

Under the first two readings, "upgrade the extractor" is a fix that the bullet's only fix ("add a resource node") leaves out. It also isn't stated whether factor may raise an unpinned extractor's mark by itself to meet demand. SC-9 only says type and purity "return to factor's default", and it doesn't say whether that default depends on demand.

**Two meanings of "cap".** D-018 line 183 records Peter's label "Cap = pinned extractor clock". Line 184, in Puck's prose, says "The cap is the extractor's derived ceiling". Those are different values whenever the clock is pinned below its maximum. The brief uses "cap" (SC-4's heading "Rounding over a cap", line 59), "ceiling" (HC-4, SC-6) and "limited input" (SC-4 line 57), and the glossary defines none of them.

**"Adds the fewest new machines" (line 64).** The glossary (line 172) makes an extractor a machine, so read literally the rule adds miners. Line 67 forbids factor from adding a resource node, and a node holds one miner. The carve-out holds only by implication.

**F-043 and F-044 are *mvp*.** Their verdict texts say "Compute how many miners/pumps/extractors a raw demand needs" and "Enter the nodes you actually have … and get miners per node". These may be how the "add a resource node" fix gets its content, but the brief doesn't connect them.

*Suggested:*
- Add a glossary entry, **Extractor ceiling**: the rate at its type, purity and the highest clock its placed shards allow.
- Use "pinned extractor clock" where the limit is meant.
- Retitle SC-4's line 59 "Display rounding against a limited input".
- Scope line 64 to manufacturers.
- Domain Question 2 covers the extractor-mark and fix-list questions.

### R4-5 · medium · fix-induced (round-6 restructure) · Rejected alternatives were dropped and now exist nowhere in `docs/`
**Anchor:** SC-3 line 52; SC-7 lines 74 and 75; SC-8 line 78; SC-6 lines 66 and 67; SC-9 line 81; HC-11 line 123.

The restructure removed the "over X and Y" clauses. Range: `grep -n -e 'Under 250' -e 'No bound' -e 'Refuse to open' -e 'Migrate automatically' -e 'explicit saves only' -e 'no criterion' docs/decisions.md docs/intent/factor.md` returns nothing. The control is the same grep with `'Overclock first'` and `'Keep current count'`, which hits D-016 line 210.

So SC-6's and SC-9's alternatives survive in D-016, but these don't:
- **SC-3's redraw:** "Under 250 ms", "No bound";
- **SC-7's game-update rule:** "Refuse to open", "Migrate automatically";
- **SC-8:** "explicit saves only", "no criterion".

They're now in git history only. Every round-6 ruling also arrives without alternatives: "Hold the pin, name a shortfall", "Name a shortfall", "Migrate forward", "Two events", "Cap = pinned extractor clock" and "Strip to outcomes". Only "Two events" names what it was chosen over, by implication (one gate).

The next reader of any of these can't tell what Peter turned down. HC-10 kept its alternatives, so the brief's shape is inconsistent about this as well.

*Suggested:* restore the "over …" clauses, or move each choice and its alternatives into the `decisions.md` block it refines. D-016 already does this for SC-6.

### R4-6 · low · fix-induced (round-6 restructure) · Four removed checks have no carrier, and one of them is a product behaviour
**Anchor:** FQ-10 lines 207–213; HC-10 lines 117–122; SC-3 line 53.

The FQ-10 intro says it "takes in the mechanics the reviews raised". These were removed and don't appear in FQ-10 or anywhere else in the brief:
- **"Solve time is also recorded on every solve"** (old SC-3 check). This is runtime instrumentation, which the observability value wants at first use, not a test mechanic. Stripping it as mechanics drops a product behaviour.
- **"Each measurement records its model, chip and memory"** (old SC-3). This was N12's round-2 fix, so it has regressed.
- **"Timed … by an instrument outside the solver"** (old SC-3 check).
- **HC-10's check:** "at each Spec, measured contrast for the tokens in use, and a keyboard-only walk of the SC-3 edit loop". FQ-10 covers success criteria only, so an HC check has no carrier at all.

SC-8's old process-kill and integrity check has thinned to "a storage seam to simulate power loss" in FQ-10. The integrity check on reopen isn't named.

*Suggested:*
- Put the solve-time record back as an outcome under SC-3.
- Add the other three to FQ-10's list.
- Widen FQ-10's scope to "each success criterion and hard constraint".

### R4-7 · low · fix-induced (round-6 restructure and HC-11) · Labels lost, and HC-11's gate assignments carry no source
**Anchor:** SC-2 line 49; glossary line 172; SC-4 line 59; HC-11 lines 123–129.
- **SC-2's machine count.** The old bullet said miners, extractors and generators count "(**Puck's reading**)". Now SC-2 says "see Glossary", and the glossary states it as a bare definition, so the label is gone.
- **SC-4's 0.00005 bound** lost "(Puck's arithmetic)". "Peter chose 'Say nothing'" also lost the question it answered, which was whether factor should flag a rounded clock that draws over a limited input. On its own line it reads as "say nothing" about the bound in general.
- **HC-11.** "Two events" is Peter's label. Which obligation goes to which gate, and the new item "signed and notarised releases", carry no source.
  - **Search range:** `grep -rn -e 'Two events' docs scratch CLAUDE.md` hit only brief line 123, run before this file existed (this file now matches too). The commit bodies of `2dcf4b0`, `82b7f00` and `e8912b4` are title-only.
  - I couldn't establish whether the option text carried the assignments, so this stays **unverified**, not resolved.
  - HC-10's "At Gate B" mapping of Peter's "enforce on share" has the same exposure.

*Suggested:* label each as **Puck's reading**, or cite the round-6 option text.

### R4-8 · low · fix-induced (round 6: SC-7 split) · SC-7 lost its noun, and the format version has no newer-file case
**Anchor:** SC-7 lines 72–76.
- **"A file that is corrupt…"** replaced "a malformed or invalid data file or plan file". The scope is now every file factor or its tools read: the raw bundle the generator reads, icon archives and save files (RP-1). "Shown in the app" can't hold for the generator, which is a separate binary under D-003. The old fixture list's "malformed Unreal-serialised string" is a generator-input case, so the old text did reach it.
- **A plan saved by a *newer* factor.** Plan files now carry a format version, and the three-way split covers corrupt, game-updated and older. A newer file could be read as "corrupt" (rejected), or opened with whatever is unknown named. My reasoning, not FQ-4's: this can happen with Peter as the only user, if he runs factor on two Macs at different versions or rolls a build back. FQ-4's "new Mac" example is the older-format case (Domain Question 5).

### R4-9 · low · residuals and small trips
- **SC-3's edit list (R3-1 residual, fix-induced).** "A change to an extractor's settings, or setting or releasing a pin." Extractor type, purity and clock are now pin kinds (SC-9), so the second item is a subset of the third.
- **FQ-9 line 204.** "A local model for F-119, before anyone else uses factor (WTB-11)" is a Gate B timing that Gate B's list doesn't include. RP-3 also routes F-119 per slice. One of the two should own it.
- **SC-6's "Puck's reading" (line 70).** "Kept counts are part of the stored plan" dropped "and survive closing and reopening it", which was the observable half.
- **SC-2's memory bound.** "With the plan loaded, solved and edited" became "at peak", which no longer says at peak *of what*.
- **"Machine recipe", 291 (R3-9, still open).** The glossary makes extractors and generators machines, but the 291 counts manufacturer recipes (CLAUDE.md: "291 are made in a machine").
- **HC-4's "never typed" (R3-9, still open).** R4-2 makes this sharper: F-007 types a raw amount, and Peter types the extractor clock as a percentage (D-018 quote). "Never entered directly; it follows from the extractor's type, purity and clock" says what's meant.
- **Glossary "Release note" (R3-9, still open).** It names two labels where the register uses three.
- **Outside the brief:** D-024's Outcome still has "cap an input", and D-016's "Refined" entry still has "after a target or cap change".

## Domain Questions

1. **Shards you've placed (R4-1).** You've put a shard in a smelter but haven't set its clock, and then you raise the target past what the kept machines make at 100%. What should factor do with that smelter, and where does F-032's shard budget fit with "unless i ask for it to be sharded"?
2. **When one node runs out (R4-4).** You haven't chosen the miner's mark, and demand goes past what it gives on its node. What fixes should factor offer, and what may it change about the miner without asking?
3. **Scaling to what you have (R4-2).** F-007 lets you type how much of a raw resource you have and scales the targets to it. Now that a resource is limited by the extractor clock, how do you want to tell factor what you have? And when factor works out the output for you, what should happen to that output when you then change something else?
4. **A build before a public repo (R4-3).** If you hand a build to a friend before the repo has a public remote, which of the licence, game-data and icon questions should be settled before that happens?
5. **A plan from a newer factor (R4-8).** If you open a plan saved by a newer version of factor than the one you're running, for example on a second Mac that's behind, what should happen?
