# Glitch review, round 3: docs/intent/factor.md (Intake, product altitude)

Lens: testability, external observability, whether each criterion can fail for the right reason.
Read: the brief in full; `scratch/factor-review-r2/glitch.md`; `docs/design/ui-brief.md` §7 (lines 219-250); `docs/decisions.md` D-018 (line 176), D-016, D-022, D-033.
Nothing was run. All arithmetic below is by hand from the §7 recipes and the D-018 miner figures (Mk.2 120/min). The base rates (plate constructor 20/min, rod 15, screw 40, assembler 5, smelter 30) are carried from my round-2 arithmetic over the §7 recipes. I did not re-read them from the game data.

## Fixture recomputation (SC-4, SC-6) under the Miner Mk.2 Normal framing

Miner Mk.2 on a Normal node is 120/min at 100% (D-018). Pinned at 2/3, that gives 80/min. **The 80/min cap is unchanged, so every downstream figure from round 2 holds.**

- First solve, 7.5/min: ore 90/min, which is one Mk.2 at 3/4 (75%). Smelters x3 at 100%. Plates x3, rods x2, screws x3 and assemblers x2 at 75%. This matches the brief and §7.
- Pin the miner at 2/3: ore 80/min. Smelters 80/90 = 8/9. Downstream 3/4 x 8/9 = 2/3. Reinforced Iron Plate = 80/12 = 20/3. Shortfall = 7.5 - 20/3 = 5/6. **SC-4 steps 1 to 3 are arithmetically correct.**
- SC-6 contrast: plates 40/min over 3 constructors = 2/3 (kept). Re-minimised it would be 2 at 100%. Screws 80/min likewise (3 at 2/3 versus 2 at 100%). Rods, assemblers and smelters cannot discriminate keep from re-minimise. This is unchanged. The SC-6 check names plates, which is right.
- **SC-6 raise to 10/min**, starting from the first-solve state (miner unpinned):
  - Ore 120/min is one Mk.2 at exactly 100%.
  - Smelters need 4 (120/30), so 1 is added and all 4 sit at 100%.
  - Plates 60/min = 3 x 20 at 100%. Screws 120/min = 3 x 40 at 100%. Rods 30/min = 2 x 15 at 100%. Assemblers 10/min = 2 x 5 at 100%.
  - Every kept machine lands on 100% exactly and the only addition is one smelter.
  - Starting from the SC-4 step-2 state instead (miner pinned at 2/3), 10/min is capped at 80 ore and adds nothing. See F6.
- **Counter-fixture, 9/min** (same start): ore 108 (miner 1 at 90%). Smelters 108/30 = 3.6, so add 1 and run 4 at 90%. Plates 54/20 = 2.7, so 3 at 90%. Screws 108/40 = 2.7, so 3 at 90%. Rods 27/15 = 1.8, so 2 at 90%. Assemblers 1.8, so 2 at 90%. Exactly one machine is added and every clock is 9/10. This exercises "re-clock all evenly" and "no new machine where kept ones suffice".

## Round-2 dispositions

- **F1 (SC-2 scale dimension):** resolved. Recipe nodes >= 2,000 and machines >= 5,000 bound both dimensions. Residuals are fix-induced: F4 (oracle versus connectedness) and F12 (machines are a solved output).
- **F2 (SC-2 no oracle):** partly resolved. A known-answer oracle is stated, but its composition is deferred to FQ-7 and it is in tension with "one connected plan". See F4.
- **F3 (SC-3 window):** partly resolved. The exact re-check is now inside the window (resolved). The edit mix and sample count are now an explicit Frame call (acceptable). Still open: "largest connected part" is the whole plan, edit locations are unspecified, and "a result over 100 ms is a failure" conflicts with p95. See F2.
- **F4 (SC-6 / SC-9 release):** resolved. Release re-minimises that node. Fix-induced residual: release is undefined for some of the newly covered kinds (F9).
- **F5 (SC-6 boundary):** mostly resolved. The rise rule is ruled, and the fall rule and persistence are labelled Puck's reading. Residuals are F6 (check weakness and start state) and Domain Question 4 (extractor ceiling).
- **F6 (SC-8 check coverage):** mostly resolved. Process crash and power loss are split, seeded points are stated, and "completed" is defined. Fix-induced residuals are F7 and F8.
- **F7 (SC-7 taxonomy):** resolved by the seeded list. It is now internally inconsistent with the game-update paragraph (F1) and presupposes FQ-4 (F10).
- **F8 (SC-9 view artefact):** resolved by "Marks belong to the data".
- **F9 (smaller items):**
  - Mac model: resolved (recorded per measurement).
  - Memory peak: resolved ("all processes together").
  - Fixture 2 x 75% example: still not in the check (low, acceptable; the iron chain has 75% cases).
  - The keep-versus-re-minimise negative assertion: resolved.
  - Residual: how "memory" is measured on macOS is unstated (RSS counts shared pages; physical footprint does not). Low.

## Findings

### F1 (high, fix-induced) SC-7: one fixture, two required outcomes
Anchor: SC-7 first paragraph and Check list versus the "valid plan that refers to recipes or items a game update removed" paragraph.
The Check list includes "a missing reference", which must be rejected whole with no partial plan. The new game-update paragraph says a valid plan whose recipe or item reference is gone **opens**, with each affected node a named problem. A plan whose recipe id is absent from the loaded game data is a missing reference. A test author gets both verdicts from the same fixture. "Renamed" is also undetectable as a rename without an alias map. It looks identical to removed, so only "removed" is testable.
Fix: split the fixture class by what is missing.
- Reference to a game-data entity absent from the loaded data: opens, named problem per node, nothing dropped. Add this as its own seeded fixture, with an assertion that the node count after open equals the stored node count.
- Reference inside the file itself (an edge to a nonexistent node, or a missing owner row): rejected whole.
Also state whether the rest of the plan solves with the unresolved nodes excluded or held, because the rest of the numbers are otherwise undefined.

### F2 (medium, partly fix-induced) SC-3 window: three residual ambiguities
Anchor: SC-3 Window and Check.
- "Largest connected part (its biggest connected group of recipe nodes)" is the entire plan, because SC-2 defines one connected plan. The phrase either carries no information or it means an LP coupling component. Say which. D-017's incremental recompute is exactly what makes an edit at a leaf cheap and an edit near the target expensive.
- Edit **locations** are unspecified. Edit kinds are named, but a p95 over edits all made at cheap leaf sites passes while the worst-case site fails. Require that the scripted mix includes edits at the most-coupled sites (for example a target at the end of the longest chain, or a node on a byproduct loop), and name them in the Check.
- "A result over 100 ms is a failure, not a warning" conflicts with a p95 criterion, since 5% of samples may legitimately exceed 100 ms. Read as "a p95 over 100 ms is a failure", it is fine. Reword so the failing statistic is explicit. (Fix-induced by the new sentence.)

### F3 (medium, fix-induced) SC-3 stale marking cannot fail at nominal speed, and the redraw bound has no check
Anchor: SC-3 Redraw and Check.
- "Previous numbers visibly marked as stale, never shown as current." If the solve meets 100 ms, the stale state exists for under 100 ms and a test cannot reliably observe it. The criterion can only fail on a slow run, which is when nobody is asserting it. It also has two problems under HC-6 (replaceable view): "visibly" is a pixel, and no queryable attribute exists. Fix: make staleness a queryable attribute of the displayed numbers, like pin marks. Then a test with an injected solve delay (a test-only seam, never a production hook) can assert stale, then current, in order, and assert that no value is ever reported current against an older solve.
- The 1-second redraw has no Check line. The Check times "edit to updated numbers" only. Say what measures redraw (an instrument outside the solver and outside the view code, per the SC-3 Check) and whether the same scripted mix drives it.
- "Visible" in "numbers visible in under 100 ms" still names no observable surface (round-2 F8, F1). It matters now that two clocks (100 ms and 1 s) are defined against two different surfaces.

### F4 (medium, fix-induced) SC-2 oracle versus "one connected plan"
Anchor: SC-2 solves; FQ-7.
The oracle is "composed from fixtures whose answers are known". A plan composed of independent known-answer blocks is not one connected plan. To connect them you need a shared supply, a shared byproduct sink or cross-links, and each of these changes the answer (the LP couples them), so the sum of block answers stops being the oracle. If instead the blocks are joined only trivially, then D-017's incremental recompute touches one block per edit, and the SC-3 workload on it is far smaller than megabase. Both outcomes defeat the criterion. Carry this into FQ-7 as a stated constraint:
- the join must preserve the oracle (for example uncapped shared supply, with the join shown not to bind);
- the largest edit-reachable component must still be megabase-sized, and the Check must state that size.
Two further points:
- Where the LP has ties, "returns the plan its known answer predicts" is unfalsifiable at machine-assignment level. The Check should assert the objective, the rates, the named problems and the machine counts only where the optimum is unique.
- "Every machine recipe in the game: 291" is a number from today's bundle. The Check must derive it from the loaded data, or SC-7's game-update case will turn SC-2 red for the wrong reason.

### F5 (medium, fix-induced) SC-4 fixture setup omits the miner, and "from the game data" is only partly true
Anchor: SC-4 Check steps 1 to 2; D-018.
Step 1 lists no miner. D-018 says "factor picks a default and I can change it". A default Mk.1 (60/min) on a Normal node cannot supply the 90 ore/min that 7.5/min needs from one node (one extractor per node), so step 1's expected result depends on a default nobody has ruled. Fix: step 1 sets the miner as an explicit input (Mk.2, Normal), and also asserts the miner's first-solve clock (3/4, one machine).
Also, the Check says fixtures are "built from the game data". The Normal x1 purity multiplier is game knowledge, not in the data (D-018 says so; CLAUDE.md says `mPurityMultiplier` has zero hits). Label that input in the Check.
(`ui-brief.md` §7 still says "Iron Ore (free up to cap)". That is already routed to the design work.)

### F6 (medium, partly fix-induced) SC-6 raised-target check is weak and its starting state is unnamed
Anchor: SC-6 Check, second bullet.
"Raising the target from 7.5 to 10/min adds machines, with none above 100%" has three problems.
- It names no start state. From the SC-4 step-2 state (miner pinned at 2/3) 10/min adds nothing and is capped at 80 ore, so the assertion fails for the wrong reason.
- From the first-solve state, 10/min makes every kept machine land on exactly 100%. The result is one added smelter and the boundary value everywhere. It cannot show "re-clock evenly" and sits exactly on the "at or below 100%" edge, so it would pass an implementation with a `<=` versus `<` mistake in either direction. It does discriminate against overclock-first (smelters would be 133%).
- "Adds machines" is not an assertion. Assert the exact result: smelters x4 at 100%, plates x3, rods x2, screws x3 and assemblers x2 at 100%, miner x1 at 100%.
Fix: name the start state, assert the exact result at 10/min as the boundary case, and add 9/min as the non-boundary case (one smelter added, every clock 9/10; figures above).

### F7 (medium, fix-induced) SC-8: the durable write precedes "displayed", so it sits inside SC-3's window
Anchor: SC-8 (completed edit, crash), SC-3.
"A completed edit is one whose new numbers were displayed" and "if factor crashes, reopening shows every completed edit." For that to hold, the edit's write must reach the OS (the database commit) **before** the numbers are displayed. That write is therefore inside the 100 ms window. The brief says only that the **sync** (fsync) runs outside the window. A process crash needs the commit and not the sync, so the commit cost is inside the window and unstated. Also, "displayed" is a view event. Under HC-6 the test needs an observable that marks "completed" without reading pixels (a backend acknowledgement event or log record). Fix: state that the commit is inside the window and the fsync is outside, and name the completed-edit signal as a backend-readable event.

### F8 (medium, fix-induced) SC-8 power-loss check and the sync interval need a seam, and the sync must be observable
Anchor: SC-8 Check, second bullet.
"Simulate an abrupt stop that discards unsynced writes" cannot be done by killing the process. After a kill -9 the OS still holds the written pages, so nothing is discarded. It needs a fault-injecting storage layer (a lossy VFS shim) or a block-level snapshot. Propose a test-only feature gate or a test-support crate for this, never a production hook. This is a finding rather than a licence to reach inside.
To assert "loses at most the edits since the last sync", the test must know where the last sync was. Require that each sync is externally observable (a log or event record with the edit sequence number).
Also state the valid range of the sync-interval setting: zero, negative, absurdly large, and "10 s or 10 edits, whichever first" with only one half configured. Config input is a trust boundary under SC-7's own logic.

### F9 (medium, fix-induced) SC-9 release is undefined for some of the newly covered pin kinds
Anchor: SC-9 "every kind of value he can set" and the Check "observe the value return to factor's choice".
- Miner or extractor settings include purity and mark. D-018 says factor picks a default and Peter can change it, but the Normal purity of a real resource node is a fact about the world and not a choice of factor's. "Factor's choice" after release is a default guess. Is it re-guessed or reset?
- A pinned **target rate** has no "factor's choice". Releasing it either removes the demand or does nothing.
- A released **recipe** pin returns to the solver's choice, which depends on the D-023 objective. The fixture must be one where that choice is unique.
Fix: for each kind, the Check states what the post-release value is, or states that the kind is not releasable and what "release" means for it. Otherwise the all-kinds loop in the Check has no oracle for these three.

### F10 (medium, fix-induced) SC-7 presupposes FQ-4's answer
Anchor: SC-7 Check ("an unknown or foreign owner id"), RP-2, FQ-4.
The Check requires a plan with a foreign owner id to be rejected. FQ-4 asks what owner id an imported plan gets and carries the question to Frame, and RP-1 says foreign plan files are not in the first build. If the answer to FQ-4 is "re-owned on import", the fixture is wrong. Either mark the fixture as conditional on FQ-4, or make rejection a ruled constraint now.

### F11 (low) SC-2 has no time bound on load or the first solve, and SC-3 excludes re-minimise
Anchor: SC-2 loads, solves; SC-6.
SC-2 "opens" and "solves" have no time bound. A first solve that takes ten minutes and an open that takes one both pass. SC-3 times only edits. The explicit re-minimise action (SC-6) is an edit-adjacent action and falls under neither. Peter's failure was "dies", so "completes within memory" may be the deliberate bar. If so, say it. If not, add bounds, which may be left to Frame. Not stated either way today.

### F12 (low, fix-induced) SC-2: 5,000 machines is a solved output, not a plan input
Anchor: SC-2 machines.
Counts are sized after the solve (D-016), so "at least 5,000 production machines" is true of the reference plan only for a particular target set. The Check should assert it on the solved reference plan, with the count taken by an instrument (excluding belts, splitters, mergers, lifts and poles, including miners and generators). Otherwise a changed target set or game data version makes the plan silently smaller than the criterion. Also say whether extraction recipes count toward the 2,000 recipe nodes (D-018 makes extraction a recipe).

### F13 (low) SC-5: bug fixes versus extension, and the extension list itself
Anchor: SC-5.
A defect in the core found while adding game 2 and fixed there is a "core change" outside an extension point and fails SC-5 as written. Say whether a fix that adds no game-specific behaviour counts. The list of declared extension points (FQ-6) is the baseline of the diff check. Add that changing the list after the second game's work starts is itself a core change. The diff check does not fire until the list exists, and the brief says it must be declared before the work starts, which is the tripwire. Acceptable at Intake.

### F14 (low) SC-7 "oversized", "hang", "without bound" have no numbers
Anchor: SC-7.
Valid megabase plans are large (SC-2), so "oversized" needs a threshold above that plan. "Hanging" needs a wall-clock bound. "Memory growth" needs a ceiling relative to input size. Frame calls are fine, but name them as open or the fixture author picks easy values.

## Fix-induced accounting

Fix-induced: F1, F3, F4, F5, F7, F8, F9, F10, F12 fully. F2 and F6 partly. Not fix-induced: F11, F13, F14.
Of 14 findings, 11 are fully or partly fix-induced. Severity is lower than round 2 (one high, which is a direct contradiction). Most fix-induced items sit on the new SC-7, SC-8 and SC-9 text, not on SC-1 through SC-6.

## Domain Questions

1. **SC-7 (F1):** when a plan references a recipe or item absent from the loaded game data, it opens with a named problem. When the file itself is internally inconsistent (an edge to a nonexistent node), it is rejected whole. Is that the intended split? If so, state the split in the criterion.
2. **SC-7 / FQ-4 (F10):** is rejection of a plan file with a foreign owner id a ruled first-build constraint, or is it conditional on how FQ-4 resolves?
3. **SC-8 / SC-3 (F7):** the database commit that makes an edit durable against an app crash happens before its numbers are displayed. Is that commit inside the 100 ms window, with only the fsync outside?
4. **SC-6 (F6):** the one Mk.2 Normal node saturates at 120/min, which is a 10/min target. For a target above that (for example 12/min), does factor name a shortfall at the extractor ceiling, or add another resource node? One extractor per node means "add the fewest new machines" cannot apply to the miner.
5. **SC-9 (F9):** what does releasing a pinned purity, mark or target rate mean? Does it reset, re-guess, or is the kind not releasable?

[ARCH-DEFERRED]: none of the above prescribes a framework, runner or storage mechanism. The test-only seam proposals in F3 and F8 are existence arguments, and the form is for Frame.
