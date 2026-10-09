# Glitch review, round 2: docs/intent/factor.md (Intake, product altitude)

Lens: testability of the success criteria, external observability, whether each can fail for the right reason.
Read: the brief; `scratch/factor-review-r1/glitch.md`; `docs/design/ui-brief.md` §7 (lines 219-250); `docs/decisions.md` D-008 (lines 77-86).
Nothing was run. The fixture arithmetic below is by hand from the recipes in ui-brief §7.

## Fixture recomputation (SC-4, SC-6)

Base rates from the §7 recipes: Smelter 30 ingots/min; Plate constructor 3 ingots -> 2 plates in 6 s = 20 plates/min; Rod constructor 15/min; Screw constructor 1 rod -> 4 screws in 6 s = 40 screws/min; Assembler (Reinforced Iron Plate, 6 plates + 12 screws) 5/min.
The base rates are my arithmetic from the §7 recipes and durations, not read from the game data.

- First solve, 7.5/min: 45 plates -> 2.25 -> 3 constructors at 75%. 90 screws -> 2.25 -> 3 at 75%. 22.5 rods -> 1.5 -> 2 at 75%. 1.5 assemblers -> 2 at 75%. Ingots 67.5 + 22.5 = 90 -> 3 smelters at 100%. **Matches the §7 table.**
- Ore cap 80/min: each Reinforced Iron Plate costs 12 ingots (9 for plates, 3 for screws via rods), so 80/12 = 6.6667/min = 20/3. Shortfall 7.5 - 20/3 = 5/6 = 0.8333. Smelters 80/(3x30) = 8/9. Downstream 3/4 x 8/9 = 2/3. **All stated figures are correct, in the SC-4 sentence and in §7.**
- SC-6 keep-counts: plates 3 x 2/3, screws 3 x 2/3, rods 2 x 2/3, assemblers 2 x 2/3, smelters 3 x 8/9.
- Contrast (re-minimise at the capped rate): plates 40/min = **2 at 100%**, screws 80/min = **2 at 100%**, rods 20/min = 2 at 2/3, assemblers = 2 at 2/3, smelters = 3 at 8/9. So the fixture discriminates "keep" from "re-minimise" on plates and screws only. The SC-6 check names plates, which is right. Smelters, rods and assemblers cannot discriminate.
- Display at 4 dp rounds to nearest: 2/3 -> 66.6667%, 8/9 -> 88.8889%. A test must assert the clocks on the exact fraction exposed "on request", not on the display string. 3 x 30 x 0.888889 = 80.00001, so a display-value assertion would encode the overdraw that Peter's ruling accepts.

## Round-1 dispositions

- F1 (SC-3 under-specified): **partly resolved.** Statistic (p95), hardware ("Peter's Mac"), edit kinds, warm-only (edits) and an end point ("numbers visible") are now stated. Still open: edit-mix proportions and sample count, the Mac model, and what "visible" means with the toolkit open (D-036). See F3 below.
- F2 (aspiration vs gate): **partly resolved.** The relax-by-recorded-decision clause stays. The brief still does not say that red against 100 ms is the intended state until a decision relaxes it. Low now.
- F3 (SC-2 undefined): **partly resolved.** Machine unit, memory bound, reference-plan definition and the three outcomes are added, and generation is carried to Q-F7. Fix-induced gaps in F1 and F2 below.
- F4 (SC-4 exact vs rounded vs overdraw): **resolved.** Peter ruled round-to-nearest, the exact value is exposed, and the fixture is defined and arithmetically correct. Residual: the "never overdraw" clause has no observable at display precision, only on the exact plan. The brief says so, so this is fine. "Values the game accepts" still names no source of truth (low).
- F5 (SC-5 diff check, vacuous): **partly resolved.** Timing is fixed (checked when the second game is added) and a known-answer reference plan is added. The diff check still depends on the declared-extension-point list, which is deferred to Q-F6. It cannot fail until that list exists. The brief says "declared before that game's work starts", so there is a tripwire. Acceptable at Intake.
- F6 (SC-1 trigger): **resolved.** The trigger is named and a "no" names the missing capability.
- F7 (SC-3 vs D-022 exact recheck): **not resolved.** The brief does not say whether the exact-rational recheck is inside the 100 ms window. "Recomputed numbers" arguably includes the exact value, which D-022 produces after the recheck. See F3 below.
- F8 (SC-3 external surface): **partly resolved.** "An instrument outside the solver" is stated, but the surface is not named. The ui-brief status bar already shows solve time, which is a candidate observable. Low.
- F9 (NG-4, HC-1 unchecked): **resolved by acknowledgement** (carried as a known low limitation).
- F10 (load-time validation): **resolved by SC-7.** Residual gaps in F7 below.

## Findings

### F1 (high, fix-induced) SC-2 cannot fail on the dimension that breaks Modeler
Anchor: SC-2 (machine definition), SC-3 "Not a contradiction with EV-3" bullet.
The brief states that the solve size does not grow with machine count, because counts are sized after the solve (D-016): "5,000 machines do not enlarge the solve." That is probably true. It means the SC-2 threshold is measured on a dimension that does not stress the engine. Peter's failure ("can't calculate all the nodes on a change") scales with distinct recipe instances, items and factories. Those are the quantity EV-3's 300-copies model scaled, and SC-2 does not bound them. A plan with 291 recipes at 5,000 machines is the whole-game solve (about 0.9 ms) plus larger count arithmetic. It would pass easily and prove nothing about megabase scale.
Fix: bound the solve-size dimension as well (minimum diagram nodes, columns, or factories, on a number Peter chooses or a stated Puck's reading). Or state that machine count is the scale proxy and that the LP-size dimension is deliberately not under test.

### F2 (medium, fix-induced) SC-2 "solves" has no oracle
Anchor: SC-2.
"Returns an exact plan in which every shortfall, surplus and unhandled byproduct is named" is a shape, not a correct answer. A generated 291-recipe connected plan has no known-good output, so a solver that returns a wrong but fully annotated plan passes. D-022's exact recheck only checks internal consistency, not that the plan is optimal or correct.
Fix: build the reference plan by composition from fixtures with known answers (for example N scaled copies of the SC-4 iron chain, plus a known loop and a known byproduct case) so an expected total is computable. Put this in Q-F7.

### F3 (medium) SC-3 window still ambiguous on three points
Anchor: SC-3.
- "Largest connected part": SC-2 defines one connected plan, so the part is either the whole plan or an LP component. The two give different workloads, and D-017 incremental recompute is the very thing that makes them differ. Say which.
- Exact recheck: say whether D-022's rational recheck is inside the window (carried over from round-1 F7).
- Sample count and edit-mix proportions are absent, so p95 is not computable. At the very least, name a minimum sample count.

### F4 (high, fix-induced) SC-6 and SC-9 conflict on releasing a count pin
Anchor: SC-9 "released back to factor's choice", SC-6.
SC-6 says counts stay until an explicit re-minimise. SC-9 says releasing a pinned machine count returns "the value to the solver's choice." After a release, which is factor's choice: the kept count, or the fewest-buildings count? The two scenarios assert different numbers, and the SC-9 check ("observe the value return to the solver's choice") cannot be written until this is settled. Resolve it by ruling that release keeps the count (it becomes an unmarked kept count) or that release triggers a re-minimise for that node.

### F5 (medium, fix-induced) SC-6 is silent on kept counts that cannot carry the new load
Anchor: SC-6 "only their clocks change".
If a target rises so a kept count would need a clock above the game's maximum (or the shard budget, F-032), or falls below the minimum clock, "only clocks change" is impossible. Does the count grow, does the plan report a shortfall, or is the clock capped? As written the criterion has no failing case at the boundary. The fixture only exercises a clock decrease. Also state whether counts persist across save and reopen (SC-8) or whether reopening counts as a first solve.

### F6 (medium, fix-induced) SC-8 check covers less than the criterion claims
Anchor: SC-8.
- The criterion says "factor or the Mac crashes." The check kills the process. A Mac crash (power loss) tests the fsync/durability setting, and a process kill does not. Either narrow the claim to process crash, or add a durability check.
- "Random points" is not reproducible. Require a seed logged on failure, or a deterministic sweep over every edit boundary.
- "The edit in progress" has no boundary. State the observable that marks an edit as completed (for example the numbers have been shown, or the edit call has returned) so the test knows which edits it must find on reopen.
- "The file passes an integrity check" is a storage check (for example SQLite integrity_check). Add that reopen also passes SC-7 validation.
- Cost interaction with SC-3: a durable write per edit on a 5,000-machine plan is not mentioned. State that persistence is outside the 100 ms window, or inside it.

### F7 (low-medium) SC-7 has no taxonomy and no error contract
Anchor: SC-7.
"A named error that says which file and what is wrong" has no format or enumeration. Specify a minimum set of seeded faults the criterion must cover: truncated file, wrong encoding (the bundle varies per file, including UTF-16LE without a BOM), a dangling reference, a duplicate id, an out-of-range value, a plan file with a missing or foreign owner id (Q-F4). The test plan must assert "no partial load" as an observable: no plan state exists after rejection. Without these, a test author can pick only easy fixtures.

### F8 (low) SC-9 observable is a view artefact
Anchor: SC-9, HC-6.
"Marked as his" is satisfied by a pixel under HC-6 (replaceable view). For it to be testable without a particular toolkit, the pinned/solver-chosen distinction must be a queryable attribute of the plan. Add that to the criterion.

### F9 (low) Smaller items
- SC-3 "Peter's Mac": name the machine class so a later run on a different Mac is comparable.
- SC-2 memory: say whether 1 GB is peak or steady-state resident, and whether the diagram view is included.
- SC-4 fixture gives one case. The SC-4 text cites the 2 x 75% example. Add it to the check, and add the keep-counts contrast (2 plate constructors at 100%) as the negative assertion for SC-6.

## Domain Questions

1. SC-2: what is the scale dimension that must grow, given the brief states machine counts do not enlarge the solve? Pick node/recipe-instance/factory count and a minimum, or record that machine count is the deliberate proxy. (F1)
2. SC-9 vs SC-6: when Peter releases a pinned machine count, does the count stay or does the node re-minimise? (F4)
3. SC-6: when a target change makes a kept count's clock exceed the game's maximum, does the count grow or does the plan report a shortfall? (F5)
4. SC-8: is a Mac power-loss crash in scope for the first build, or only a process crash? (F6)
5. SC-3: is the D-022 exact recheck inside the 100 ms window? (F3)

[ARCH-DEFERRED]: none of the above prescribes a framework, runner or storage mechanism.
